import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../services/auth.service';
import { PatientService, Patient, PatientCreate } from '../../services/patient.service';

@Component({
    selector: 'app-dashboard',
    standalone: true,
    imports: [CommonModule, FormsModule, MatSnackBarModule, MatProgressSpinnerModule],
    templateUrl: './dashboard.component.html',
    styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
    patients: Patient[] = [];
    loading = false;
    userEmail = '';
    deletingId: string | null = null;
    
    // New Patient Form State
    showCreateForm = false;
    creating = false;
    newPatient: PatientCreate = { name: '', age: 0, gender: 'Other' };

    constructor(
        private patientService: PatientService,
        private auth: AuthService,
        private router: Router,
        private snackBar: MatSnackBar
    ) { }

    ngOnInit(): void {
        this.userEmail = this.auth.getUserEmail() || '';
        this.loadPatients();
    }

    loadPatients(): void {
        this.loading = true;
        this.patientService.listPatients().subscribe({
            next: (pts) => { this.patients = pts; this.loading = false; },
            error: () => { this.loading = false; }
        });
    }

    toggleCreateForm(): void {
        this.showCreateForm = !this.showCreateForm;
        if (!this.showCreateForm) {
            this.newPatient = { name: '', age: 0, gender: 'Other' };
        }
    }

    createPatient(): void {
        if (!this.newPatient.name || !this.newPatient.age) {
            this.snackBar.open('Please provide a name and age', 'Close', { duration: 3000, panelClass: 'snack-error' });
            return;
        }

        this.creating = true;
        this.patientService.createPatient(this.newPatient).subscribe({
            next: (pt) => {
                this.creating = false;
                this.patients.unshift(pt);
                this.toggleCreateForm();
                this.snackBar.open('Patient record created!', 'Close', { duration: 3000, panelClass: 'snack-success' });
            },
            error: (err) => {
                this.creating = false;
                this.snackBar.open(err.error?.detail || 'Creation failed', 'Close', { duration: 4000, panelClass: 'snack-error' });
            }
        });
    }

    openPatient(patientId: string): void {
        this.router.navigate(['/patient', patientId]);
    }

    deletePatient(event: Event, patientId: string): void {
        event.stopPropagation();
        if (!confirm('Delete this patient and ALL their associated medical records? This cannot be undone.')) return;
        this.deletingId = patientId;
        this.patientService.deletePatient(patientId).subscribe({
            next: () => {
                this.patients = this.patients.filter(p => p.patient_id !== patientId);
                this.deletingId = null;
                this.snackBar.open('Patient fully deleted', 'Close', { duration: 2000 });
            },
            error: () => { this.deletingId = null; }
        });
    }

    formatDate(iso: string): string {
        return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }

    logout(): void {
        this.auth.logout();
    }
}
