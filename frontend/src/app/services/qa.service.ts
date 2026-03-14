import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface AskResponse {
    answer: string;
    sources: string[];
    doc_id: string;
    question: string;
}

@Injectable({ providedIn: 'root' })
export class QaService {
    private apiUrl = `${environment.apiUrl}/qa`;

    constructor(private http: HttpClient) { }

    askQuestion(docId: string, question: string): Observable<AskResponse> {
        return this.http.post<AskResponse>(`${this.apiUrl}/ask`, {
            doc_id: docId,
            question,
        });
    }
}
