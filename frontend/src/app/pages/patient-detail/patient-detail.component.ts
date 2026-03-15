import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { QaService, AskResponse } from '../../services/qa.service';
import { DocumentService, Document } from '../../services/document.service';
import { PatientService, Patient } from '../../services/patient.service';

interface ChatMessage {
    type: 'user' | 'ai';
    content: string;
    sources?: string[];
    timestamp: Date;
}

@Component({
    selector: 'app-patient-detail',
    standalone: true,
    imports: [CommonModule, FormsModule, MatSnackBarModule, MatProgressSpinnerModule],
    templateUrl: './patient-detail.component.html',
    styleUrls: ['./patient-detail.component.scss']
})
export class PatientDetailComponent implements OnInit {
    @ViewChild('chatEnd') chatEnd!: ElementRef;

    patientId = '';
    patient: Patient | null = null;
    documents: Document[] = [];
    messages: ChatMessage[] = [];
    question = '';
    
    // UI States
    loading = false;
    loadingPatient = true;
    uploading = false;
    deletingDocId: string | null = null;
    
    expandedSources: Set<number> = new Set();

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private qaService: QaService,
        private docService: DocumentService,
        private patientService: PatientService,
        private snackBar: MatSnackBar
    ) { }

    ngOnInit(): void {
        this.patientId = this.route.snapshot.paramMap.get('id') || '';
        this.loadPatientData();
    }

    loadPatientData(): void {
        this.loadingPatient = true;
        
        // Load Patient profile
        this.patientService.getPatient(this.patientId).subscribe({
            next: (pt) => {
                this.patient = pt;
                // Once patient is loaded, load their documents
                this.loadDocuments();
            },
            error: () => {
                this.loadingPatient = false;
                this.snackBar.open('Patient not found', 'Close', { duration: 3000, panelClass: 'snack-error' });
                this.router.navigate(['/dashboard']);
            }
        });
    }

    loadDocuments(): void {
        this.docService.listDocuments(this.patientId).subscribe({
            next: (res) => {
                this.documents = res.documents;
                this.loadingPatient = false;
            },
            error: () => {
                this.loadingPatient = false;
            }
        });
    }
    
    // --- Document Uploading in Sidebar ---

    onFileSelected(event: Event): void {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;
        const file = input.files[0];
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            this.snackBar.open('Only PDF files are supported', 'Close', { duration: 3000, panelClass: 'snack-error' });
            return;
        }
        
        this.uploading = true;
        this.docService.uploadDocument(this.patientId, file).subscribe({
            next: (doc) => {
                this.uploading = false;
                this.documents.unshift(doc);
                this.snackBar.open(`"${doc.filename}" added to patient record!`, 'Close', { duration: 3000, panelClass: 'snack-success' });
                input.value = '';
            },
            error: (err) => {
                this.uploading = false;
                this.snackBar.open(err.error?.detail || 'Upload failed', 'Close', { duration: 4000, panelClass: 'snack-error' });
            }
        });
    }
    
    deleteDocument(docId: string): void {
        if (!confirm('Delete this record?')) return;
        this.deletingDocId = docId;
        this.docService.deleteDocument(docId).subscribe({
            next: () => {
                this.documents = this.documents.filter(d => d.doc_id !== docId);
                this.deletingDocId = null;
            },
            error: () => { this.deletingDocId = null; }
        });
    }

    // --- Chat Logic ---

    sendQuestion(): void {
        if (!this.question.trim() || this.loading) return;
        if (this.documents.length === 0) {
            this.snackBar.open('Please upload at least one record before asking questions.', 'Close', { duration: 3000, panelClass: 'snack-error' });
            return;
        }

        const userMsg: ChatMessage = { type: 'user', content: this.question, timestamp: new Date() };
        this.messages.push(userMsg);
        const q = this.question;
        this.question = '';
        this.loading = true;
        this.scrollToBottom();

        this.qaService.askQuestion(this.patientId, q).subscribe({
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

    formatSize(bytes?: number): string {
        return this.docService.formatFileSize(bytes);
    }

    formatTime(date: Date): string {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
}
