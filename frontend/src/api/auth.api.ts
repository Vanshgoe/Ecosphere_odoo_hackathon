import { jsonRpc } from './client';
import type { CurrentUser } from '../types/api';

export const getCurrentUser = () => jsonRpc<CurrentUser>('me');
