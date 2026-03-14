import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

interface AuthResponse {
    access_token: string;
    token_type: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
    private apiUrl = environment.apiUrl;
    private TOKEN_KEY = 'ai_knowledge_token';
    private USER_EMAIL_KEY = 'ai_knowledge_email';

    constructor(private http: HttpClient, private router: Router) { }

    register(name: string, email: string, password: string): Observable<AuthResponse> {
        return this.http
            .post<AuthResponse>(`${this.apiUrl}/auth/register`, { name, email, password })
            .pipe(tap(res => this.storeToken(res.access_token, email)));
    }

    login(email: string, password: string): Observable<AuthResponse> {
        return this.http
            .post<AuthResponse>(`${this.apiUrl}/auth/login`, { email, password })
            .pipe(tap(res => this.storeToken(res.access_token, email)));
    }

    logout(): void {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_EMAIL_KEY);
        this.router.navigate(['/login']);
    }

    isLoggedIn(): boolean {
        return !!localStorage.getItem(this.TOKEN_KEY);
    }

    getToken(): string | null {
        return localStorage.getItem(this.TOKEN_KEY);
    }

    getUserEmail(): string | null {
        return localStorage.getItem(this.USER_EMAIL_KEY);
    }

    private storeToken(token: string, email: string): void {
        localStorage.setItem(this.TOKEN_KEY, token);
        localStorage.setItem(this.USER_EMAIL_KEY, email);
    }
}
