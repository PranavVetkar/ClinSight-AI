import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Document {
    doc_id: string;
    user_id: string;
    filename: string;
    page_count: number;
    chunk_count: number;
    uploaded_at: string;
    size_bytes?: number;
}

@Injectable({ providedIn: 'root' })
export class DocumentService {
    private apiUrl = `${environment.apiUrl}/documents`;

    constructor(private http: HttpClient) { }

    uploadDocument(file: File): Observable<Document> {
        const formData = new FormData();
        formData.append('file', file);
        return this.http.post<Document>(`${this.apiUrl}/upload`, formData);
    }

    listDocuments(): Observable<{ documents: Document[] }> {
        return this.http.get<{ documents: Document[] }>(`${this.apiUrl}/`);
    }

    deleteDocument(docId: string): Observable<void> {
        return this.http.delete<void>(`${this.apiUrl}/${docId}`);
    }

    formatFileSize(bytes?: number): string {
        if (!bytes) return 'Unknown size';
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }
}
