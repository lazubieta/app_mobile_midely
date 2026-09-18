vi.mock('@capacitor/preferences', () => ({
  Preferences: {
    set: vi.fn().mockResolvedValue(undefined),
    remove: vi.fn().mockResolvedValue(undefined),
    get: vi.fn().mockResolvedValue({ value: null }),
  },
}));

import { Preferences } from '@capacitor/preferences';
import { TestBed } from '@angular/core/testing';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    vi.mocked(Preferences.set).mockClear();
    vi.mocked(Preferences.remove).mockClear();
    vi.mocked(Preferences.get).mockResolvedValue({ value: null });
    service = TestBed.inject(AuthService);
  });

  it('rejects invalid credentials', async () => {
    const result = await service.login('correo-invalido', '123');
    expect(result.ok).toBe(false);
    expect(service.currentUser).toBeNull();
  });

  it('creates and clears a local session', async () => {
    const result = await service.login('demo@midely.com', 'midely123');
    expect(result.ok).toBe(true);
    expect(service.currentUser?.email).toBe('demo@midely.com');
    await service.logout();
    expect(service.currentUser).toBeNull();
  });
});
