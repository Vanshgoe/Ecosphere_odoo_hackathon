import { useState, useCallback, type ReactNode } from 'react';

/* ─── Loading ─── */
export function LoadingState({ label = 'Loading…' }: { label?: string }) {
  return (
    <div className="state state-loading" role="status" aria-live="polite">
      {label}
    </div>
  );
}

/* ─── Error ─── */
export function ErrorState({
  message,
  onRetry,
}: {
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div className="state state-error" role="alert">
      <strong>Couldn't load this data.</strong>
      <span>{message}</span>
      {onRetry && (
        <button className="button button-secondary btn-sm" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
}

/* ─── Empty ─── */
export function EmptyState({
  title,
  detail,
}: {
  title: string;
  detail: string;
}) {
  return (
    <div className="state state-empty">
      <strong>{title}</strong>
      <span>{detail}</span>
    </div>
  );
}

/* ─── Card ─── */
export function Card({
  title,
  children,
  className = '',
}: {
  title?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`card ${className}`}>
      {title && <h2 className="card-title">{title}</h2>}
      {children}
    </section>
  );
}

/* ─── Status badge ─── */
const toneMap: Record<string, string> = {
  draft: 'neutral',
  active: 'success',
  achieved: 'success',
  completed: 'success',
  approved: 'success',
  published: 'success',
  resolved: 'success',
  mitigated: 'success',
  closed: 'neutral',
  in_progress: 'info',
  submitted: 'info',
  joined: 'info',
  calculated: 'info',
  open: 'warning',
  overdue: 'danger',
  failed: 'danger',
  cancelled: 'neutral',
  requested: 'info',
  rejected: 'danger',
  registered: 'info',
  attended: 'success',
  // Severity tones
  low: 'success',
  medium: 'warning',
  high: 'danger',
  critical: 'danger',
};

export function StatusBadge({
  children,
  value,
  tone,
}: {
  children: ReactNode;
  value?: string;
  tone?: 'success' | 'warning' | 'danger' | 'info' | 'neutral';
}) {
  const resolved = tone ?? (value ? toneMap[value] ?? 'neutral' : 'neutral');
  return <span className={`status status-${resolved}`}>{children}</span>;
}

/* ─── Progress bar ─── */
export function ProgressBar({ value }: { value: number }) {
  const clamped = Math.max(0, Math.min(100, value || 0));
  return (
    <div className="progress" role="meter" aria-valuenow={clamped} aria-valuemin={0} aria-valuemax={100}>
      <span style={{ width: `${clamped}%` }} />
      <em>{clamped.toFixed(0)}%</em>
    </div>
  );
}

/* ─── Pagination ─── */
export function PaginationControls({
  total,
  limit,
  offset,
  onPage,
}: {
  total: number;
  limit: number;
  offset: number;
  onPage: (offset: number) => void;
}) {
  if (total <= limit) return null;
  const page = Math.floor(offset / limit) + 1;
  const pages = Math.ceil(total / limit);
  return (
    <div className="pagination">
      <button
        disabled={offset <= 0}
        onClick={() => onPage(Math.max(0, offset - limit))}
        aria-label="Previous page"
      >
        ‹ Prev
      </button>
      <span>
        Page {page} of {pages}
      </span>
      <button
        disabled={offset + limit >= total}
        onClick={() => onPage(offset + limit)}
        aria-label="Next page"
      >
        Next ›
      </button>
    </div>
  );
}

/* ─── Confirm dialog ─── */
export function ConfirmDialog({
  open,
  title = 'Are you sure?',
  message,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  danger = false,
  loading = false,
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title?: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  danger?: boolean;
  loading?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  if (!open) return null;
  return (
    <div className="modal-backdrop" onClick={onCancel}>
      <div
        className="modal modal-small"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <header>
          <h2>{title}</h2>
        </header>
        <p>{message}</p>
        <footer>
          <button
            className="button button-secondary btn-sm"
            onClick={onCancel}
            disabled={loading}
          >
            {cancelLabel}
          </button>
          <button
            className={`button btn-sm ${danger ? 'button-danger' : 'button-primary'}`}
            onClick={onConfirm}
            disabled={loading}
          >
            {loading ? 'Processing…' : confirmLabel}
          </button>
        </footer>
      </div>
    </div>
  );
}

/* ─── Toast / notification ─── */
interface Toast {
  id: number;
  message: string;
  tone: 'success' | 'error' | 'info';
}

let toastId = 0;

export function useToast() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const show = useCallback(
    (message: string, tone: 'success' | 'error' | 'info' = 'info') => {
      const id = ++toastId;
      setToasts((prev) => [...prev, { id, message, tone }]);
      setTimeout(
        () => setToasts((prev) => prev.filter((t) => t.id !== id)),
        4000,
      );
    },
    [],
  );

  const dismiss = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return { toasts, show, dismiss };
}

export function ToastContainer({
  toasts,
  onDismiss,
}: {
  toasts: Toast[];
  onDismiss: (id: number) => void;
}) {
  if (!toasts.length) return null;
  return (
    <div className="toast-container" aria-live="polite">
      {toasts.map((t) => (
        <div key={t.id} className={`notice notice-${t.tone}`}>
          <span>{t.message}</span>
          <button onClick={() => onDismiss(t.id)} aria-label="Dismiss">
            ×
          </button>
        </div>
      ))}
    </div>
  );
}

/* ─── Module sub-navigation ─── */
export function ModuleSubNav({
  items,
}: {
  items: Array<{ label: string; path: string; active: boolean }>;
}) {
  return (
    <nav className="sub-nav" aria-label="Module sections">
      {items.map((item) => (
        <a
          key={item.path}
          href={item.path}
          className={item.active ? 'active' : ''}
          onClick={(e) => {
            e.preventDefault();
            window.history.pushState({}, '', item.path);
            window.dispatchEvent(new PopStateEvent('popstate'));
          }}
        >
          {item.label}
        </a>
      ))}
    </nav>
  );
}

/* ─── Capability unavailable screen ─── */
export function CapabilityUnavailable({
  module,
  title,
  detail,
}: {
  module: string;
  title: string;
  detail: string;
}) {
  return (
    <div className="placeholder-page">
      <p className="eyebrow">{module.toUpperCase()}</p>
      <h2>{title}</h2>
      <Card>
        <div className="state state-unavailable">
          <div className="unavailable-icon">🔒</div>
          <strong>Backend capability unavailable</strong>
          <span>{detail}</span>
        </div>
      </Card>
    </div>
  );
}
