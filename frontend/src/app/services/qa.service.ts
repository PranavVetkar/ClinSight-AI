import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface AskResponse {
    answer: string;
    sources: string[];
    patient_id: string;
    question: string;
}

@Injectable({ providedIn: 'root' })
export class QaService {
    private apiUrl = `${environment.apiUrl}/qa`;

    constructor(private http: HttpClient) { }

    askQuestion(patientId: string, question: string): Observable<AskResponse> {
        return this.http.post<AskResponse>(`${this.apiUrl}/ask`, {
            patient_id: patientId,
            question: question,
        });
    }
}
