import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { QaService, AskResponse } from '../../services/qa.service';
import { DocumentService, Document } from '../../services/document.service';

interface ChatMessage {
    type: 'user' | 'ai';
    content: string;
    sources?: string[];
    timestamp: Date;
}

@Component({
    selector: 'app-document-detail',
    standalone: true,
    imports: [CommonModule, FormsModule, MatSnackBarModule, MatProgressSpinnerModule],
    templateUrl: './document-detail.component.html',
    styleUrls: ['./document-detail.component.scss']
})
export class DocumentDetailComponent implements OnInit {
    @ViewChild('chatEnd') chatEnd!: ElementRef;

    docId = '';
    document: Document | null = null;
    messages: ChatMessage[] = [];
    question = '';
    loading = false;
    loadingDoc = true;
    showSources = false;
    expandedSources: Set<number> = new Set();

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private qaService: QaService,
        private docService: DocumentService,
        private snackBar: MatSnackBar
    ) { }

    ngOnInit(): void {
        this.docId = this.route.snapshot.paramMap.get('id') || '';
        this.loadDocument();
    }

    loadDocument(): void {
        this.docService.listDocuments().subscribe({
            next: res => {
                this.document = res.documents.find(d => d.doc_id === this.docId) || null;
                this.loadingDoc = false;
                if (!this.document) {
                    this.snackBar.open('Document not found', 'Close', { duration: 3000, panelClass: 'snack-error' });
                    this.router.navigate(['/dashboard']);
                }
            },
            error: () => { this.loadingDoc = false; }
        });
    }

    sendQuestion(): void {
        if (!this.question.trim() || this.loading) return;

        const userMsg: ChatMessage = { type: 'user', content: this.question, timestamp: new Date() };
        this.messages.push(userMsg);
        const q = this.question;
        this.question = '';
        this.loading = true;
        this.scrollToBottom();

        this.qaService.askQuestion(this.docId, q).subscribe({
            next: (res: AskResponse) => {
                this.messages.push({
                    type: 'ai',
                    content: res.answer,
                    sources: res.sources,
                    timestamp: new Date()
                });
                this.loading = false;
                this.scrollToBottom();
            },
            error: (err) => {
                this.loading = false;
                this.snackBar.open(err.error?.detail || 'Failed to get answer', 'Close', { duration: 4000, panelClass: 'snack-error' });
            }
        });
    }

    toggleSources(index: number): void {
        if (this.expandedSources.has(index)) {
            this.expandedSources.delete(index);
        } else {
            this.expandedSources.add(index);
        }
    }

    isSourceExpanded(index: number): boolean {
        return this.expandedSources.has(index);
    }

    onKeydown(event: KeyboardEvent): void {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendQuestion();
        }
    }

    private scrollToBottom(): void {
        setTimeout(() => {
            this.chatEnd?.nativeElement?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }

    goBack(): void {
        this.router.navigate(['/dashboard']);
    }

    formatDate(iso: string): string {
        return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }

    formatTime(date: Date): string {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
}
