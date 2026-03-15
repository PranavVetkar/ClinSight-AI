import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Patient {
    patient_id: string;
    user_id: string;
    name: string;
    age: number;
    gender: string;
    mrn?: string;
    notes?: string;
    created_at: string;
}

export interface PatientCreate {
    name: string;
    age: number;
    gender: string;
    mrn?: string;
    notes?: string;
}

@Injectable({ providedIn: 'root' })
export class PatientService {
    private apiUrl = `${environment.apiUrl}/patients`;

    constructor(private http: HttpClient) { }

    createPatient(patient: PatientCreate): Observable<Patient> {
        return this.http.post<Patient>(`${this.apiUrl}/`, patient);
    }

    listPatients(): Observable<Patient[]> {
        return this.http.get<Patient[]>(`${this.apiUrl}/`);
    }

    getPatient(patientId: string): Observable<Patient> {
        return this.http.get<Patient>(`${this.apiUrl}/${patientId}`);
    }

    deletePatient(patientId: string): Observable<void> {
        return this.http.delete<void>(`${this.apiUrl}/${patientId}`);
    }
}
