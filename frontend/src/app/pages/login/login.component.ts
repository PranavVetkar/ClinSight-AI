import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { AuthService } from '../../services/auth.service';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, RouterModule, MatSnackBarModule, MatProgressSpinnerModule],
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss']
})
export class LoginComponent {
    form: FormGroup;
    loading = false;
    showPassword = false;

    constructor(
        private fb: FormBuilder,
        private auth: AuthService,
        private router: Router,
        private snackBar: MatSnackBar
    ) {
        this.form = this.fb.group({
            email: ['', [Validators.required, Validators.email]],
            password: ['', [Validators.required, Validators.minLength(6)]]
        });
    }

    onSubmit(): void {
        if (this.form.invalid) return;
        this.loading = true;
        const { email, password } = this.form.value;
        this.auth.login(email, password).subscribe({
            next: () => this.router.navigate(['/dashboard']),
            error: (err) => {
                this.loading = false;
                this.snackBar.open(err.error?.detail || 'Login failed', 'Close', { duration: 4000, panelClass: 'snack-error' });
            }
        });
    }
}
