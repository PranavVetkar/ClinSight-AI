import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../services/auth.service';
import { DocumentService, Document } from '../../services/document.service';

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule, MatSnackBarModule, MatProgressSpinnerModule],
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
    documents: Document[] = [];
    loading = false;
    uploading = false;
    userEmail = '';
    deletingId: string | null = null;

    get totalPages(): number {
        return this.documents.reduce((sum, d) => sum + d.page_count, 0);
    }


    constructor(
        private docService: DocumentService,
        private auth: AuthService,
        private router: Router,
        private snackBar: MatSnackBar
    ) { }

    ngOnInit(): void {
        this.userEmail = this.auth.getUserEmail() || '';
        this.loadDocuments();
    }

    loadDocuments(): void {
        this.loading = true;
        this.docService.listDocuments().subscribe({
            next: res => { this.documents = res.documents; this.loading = false; },
            error: () => { this.loading = false; }
        });
    }

    onFileSelected(event: Event): void {
        const input = event.target as HTMLInputElement;
        if (!input.files?.length) return;
        const file = input.files[0];
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            this.snackBar.open('Only PDF files are supported', 'Close', { duration: 3000, panelClass: 'snack-error' });
            return;
        }
        this.uploading = true;
        this.docService.uploadDocument(file).subscribe({
            next: (doc) => {
                this.uploading = false;
                this.documents.unshift(doc);
                this.snackBar.open(`"${doc.filename}" uploaded successfully!`, 'Close', { duration: 3000, panelClass: 'snack-success' });
                input.value = '';
            },
            error: (err) => {
                this.uploading = false;
                this.snackBar.open(err.error?.detail || 'Upload failed', 'Close', { duration: 4000, panelClass: 'snack-error' });
            }
        });
    }

    openDocument(docId: string): void {
        this.router.navigate(['/document', docId]);
    }

    deleteDocument(event: Event, docId: string): void {
        event.stopPropagation();
        if (!confirm('Delete this document? This cannot be undone.')) return;
        this.deletingId = docId;
        this.docService.deleteDocument(docId).subscribe({
            next: () => {
                this.documents = this.documents.filter(d => d.doc_id !== docId);
                this.deletingId = null;
                this.snackBar.open('Document deleted', 'Close', { duration: 2000 });
            },
            error: () => { this.deletingId = null; }
        });
    }

    formatSize(bytes?: number): string {
        return this.docService.formatFileSize(bytes);
    }

    formatDate(iso: string): string {
        return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }

    logout(): void {
        this.auth.logout();
    }
}
