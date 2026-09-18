import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Preferences } from '@capacitor/preferences';
import { UserSession } from '../models/user.interface';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly storageKey = 'midely-session';
  private readonly sessionSubject = new BehaviorSubject<UserSession | null>(null);
  readonly session$ = this.sessionSubject.asObservable();

  get currentUser(): UserSession | null {
    return this.sessionSubject.value;
  }

  async restore(): Promise<void> {
    const saved = await Preferences.get({ key: this.storageKey });
    if (!saved.value) return;
    try {
      this.sessionSubject.next(JSON.parse(saved.value) as UserSession);
    } catch {
      await Preferences.remove({ key: this.storageKey });
    }
  }

  async login(email: string, password: string): Promise<{ ok: boolean; message: string }> {
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      return { ok: false, message: 'Se requiere un correo electrónico válido.' };
    }
    if (password.length < 4) {
      return { ok: false, message: 'La contraseña debe tener al menos cuatro caracteres.' };
    }

    const session: UserSession = {
      email: email.trim().toLowerCase(),
      name: email.split('@')[0],
      loggedAt: new Date().toISOString(),
    };
    this.sessionSubject.next(session);
    await Preferences.set({ key: this.storageKey, value: JSON.stringify(session) });
    return { ok: true, message: 'La sesión se inició correctamente.' };
  }

  async logout(): Promise<void> {
    this.sessionSubject.next(null);
    await Preferences.remove({ key: this.storageKey });
  }
}
