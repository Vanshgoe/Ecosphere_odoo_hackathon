import { useState, type ReactNode } from 'react';
import { useResourceList, useResourceMutations } from '../hooks/useResources';
import {
  Card,
  StatusBadge,
  PaginationControls,
  ConfirmDialog,
  EmptyState,
  ErrorState,
  LoadingState,
  ProgressBar,
  useToast,
  ToastContainer,
} from './common';
import type { ApiRecord, ListParams, ResourceName, Many2One } from '../types/api';

/* ─── Field definition ─── */
export interface FieldDef {
  key: string;
  label: string;
  kind: 'text' | 'textarea' | 'number' | 'date' | 'select' | 'boolean';
  required?: boolean;
  readOnly?: boolean;
  helper?: string;
  options?: Array<{ value: string; label: string }>;
}

/* ─── Screen configuration ─── */
export interface ResourceScreenConfig {
  title: string;
  module: string;
  resource: ResourceName;
  description: string;
  statusField?: string;
  fields: FieldDef[];
  /** Custom cell renderer. Return undefined to use default. */
  render?: (row: ApiRecord, field: FieldDef) => ReactNode | undefined;
}

/* ─── Helpers ─── */
function formatCell(value: unknown, field: FieldDef): ReactNode {
  if (value === null || value === undefined || value === '') return '—';

  // Many2One objects
  if (typeof value === 'object' && value !== null && 'id' in value && 'name' in value) {
    return (value as Many2One).name;
  }

  if (field.kind === 'boolean') {
    return value ? '✓ Yes' : '✗ No';
  }

  if (field.kind === 'number' && typeof value === 'number') {
    return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }

  return String(value);
}

function getStatusTone(
  field: string | undefined,
  row: ApiRecord,
): string | undefined {
  if (!field) return undefined;
  return row[field] as string | undefined;
}

/* ─── ResourceScreen component ─── */
export function ResourceScreen({ config }: { config: ResourceScreenConfig }) {
  const { title, module, resource, description, statusField, fields, render } =
    config;

  /* ─── State ─── */
  const [params, setParams] = useState<ListParams>({ limit: 20, offset: 0 });
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [formOpen, setFormOpen] = useState(false);
  const [editRow, setEditRow] = useState<ApiRecord | null>(null);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [viewRow, setViewRow] = useState<ApiRecord | null>(null);

  const { toasts, show, dismiss } = useToast();

  const queryParams: ListParams = {
    ...params,
    ...(statusFilter ? { status: statusFilter } : {}),
  };

  const query = useResourceList<ApiRecord>(resource, queryParams);
  const mutations = useResourceMutations<ApiRecord>(resource);

  /* ─── Column definitions (visible in table) ─── */
  const visibleFields = fields.filter((f) => f.kind !== 'textarea');
  const formFields = fields.filter((f) => !f.readOnly);

  /* ─── Handlers ─── */
  function handleFormSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    const values: Record<string, unknown> = {};
    for (const field of formFields) {
      const raw = fd.get(field.key);
      if (raw === null || raw === undefined || raw === '') continue;
      if (field.kind === 'number') {
        values[field.key] = Number(raw);
      } else if (field.kind === 'boolean') {
        values[field.key] = raw === 'true';
      } else {
        values[field.key] = String(raw);
      }
    }
    if (editRow) {
      mutations.update.mutate(
        { id: editRow.id, values },
        {
          onSuccess: () => {
            show('Record updated successfully.', 'success');
            setFormOpen(false);
            setEditRow(null);
          },
          onError: (err) =>
            show(err instanceof Error ? err.message : 'Update failed.', 'error'),
        },
      );
    } else {
      mutations.create.mutate(values, {
        onSuccess: () => {
          show('Record created successfully.', 'success');
          setFormOpen(false);
        },
        onError: (err) =>
          show(err instanceof Error ? err.message : 'Create failed.', 'error'),
      });
    }
  }

  function handleDelete() {
    if (deleteId === null) return;
    mutations.remove.mutate(deleteId, {
      onSuccess: () => {
        show('Record deleted.', 'success');
        setDeleteId(null);
      },
      onError: (err) =>
        show(err instanceof Error ? err.message : 'Delete failed.', 'error'),
    });
  }

  /* ─── Status filter options ─── */
  const statusOptions = statusField
    ? fields.find((f) => f.key === statusField)?.options
    : undefined;

  /* ─── Filtered rows for client-side name search ─── */
  const rows = (query.data?.rows ?? []).filter((row) => {
    if (!search) return true;
    const name = String(row.name ?? '').toLowerCase();
    return name.includes(search.toLowerCase());
  });

  /* ─── Module color class ─── */
  const moduleClass = `module-${module.toLowerCase()}`;

  return (
    <div className={moduleClass}>
      <ToastContainer toasts={toasts} onDismiss={dismiss} />

      {/* Header */}
      <div className="page-heading">
        <div>
          <p className="eyebrow">{module.toUpperCase()}</p>
          <h2>{title}</h2>
          <p className="page-description">{description}</p>
        </div>
      </div>

      {/* Toolbar */}
      <Card>
        <div className="table-toolbar">
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', flex: 1 }}>
            <button
              className="button button-primary btn-sm"
              onClick={() => {
                setEditRow(null);
                setFormOpen(true);
              }}
            >
              + New {title.replace(/s$/, '')}
            </button>
            <input
              type="search"
              placeholder={`Search ${title.toLowerCase()}…`}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              aria-label={`Search ${title}`}
            />
          </div>
          {statusOptions && (
            <select
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setParams((p) => ({ ...p, offset: 0 }));
              }}
              aria-label="Filter by status"
            >
              <option value="">All statuses</option>
              {statusOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          )}
        </div>

        {/* Table */}
        {query.isLoading ? (
          <LoadingState label={`Loading ${title.toLowerCase()}…`} />
        ) : query.error ? (
          <ErrorState
            message={
              query.error instanceof Error
                ? query.error.message
                : 'Unable to load data.'
            }
            onRetry={() => query.refetch()}
          />
        ) : rows.length === 0 ? (
          <EmptyState
            title={`No ${title.toLowerCase()} found`}
            detail={search || statusFilter ? 'Try adjusting your filters.' : 'Create one to get started.'}
          />
        ) : (
          <>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {visibleFields.map((f) => (
                      <th key={f.key}>{f.label}</th>
                    ))}
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row) => (
                    <tr key={row.id}>
                      {visibleFields.map((f) => {
                        const customRender = render?.(row, f);
                        if (customRender !== undefined) {
                          return <td key={f.key}>{customRender}</td>;
                        }

                        const value = row[f.key];
                        const statusVal = getStatusTone(statusField, row);

                        if (f.key === statusField && statusVal) {
                          const labelKey = `${f.key}_label`;
                          return (
                            <td key={f.key}>
                              <StatusBadge value={String(statusVal)}>
                                {String(row[labelKey] ?? statusVal)}
                              </StatusBadge>
                            </td>
                          );
                        }

                        if (f.key === 'severity' && value) {
                          return (
                            <td key={f.key}>
                              <StatusBadge value={String(value)}>
                                {String(row.severity_label ?? value)}
                              </StatusBadge>
                            </td>
                          );
                        }

                        if (f.key === 'progress_percentage') {
                          return (
                            <td key={f.key}>
                              <ProgressBar value={Number(value ?? 0)} />
                            </td>
                          );
                        }

                        return <td key={f.key}>{formatCell(value, f)}</td>;
                      })}
                      <td className="table-actions">
                        <button
                          onClick={() => setViewRow(row)}
                          title="View details"
                        >
                          👁
                        </button>
                        <button
                          onClick={() => {
                            setEditRow(row);
                            setFormOpen(true);
                          }}
                          title="Edit"
                        >
                          ✏️
                        </button>
                        <button
                          className="danger-link"
                          onClick={() => setDeleteId(row.id)}
                          title="Delete"
                        >
                          🗑
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <PaginationControls
              total={query.data?.pagination.total ?? 0}
              limit={params.limit ?? 20}
              offset={params.offset ?? 0}
              onPage={(offset) => setParams((p) => ({ ...p, offset }))}
            />
          </>
        )}
      </Card>

      {/* ─── Create/Edit modal ─── */}
      {formOpen && (
        <div className="modal-backdrop" onClick={() => setFormOpen(false)}>
          <div
            className="modal"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
          >
            <header>
              <h2>{editRow ? `Edit ${title.replace(/s$/, '')}` : `New ${title.replace(/s$/, '')}`}</h2>
              <button
                className="icon-button"
                onClick={() => setFormOpen(false)}
                aria-label="Close"
              >
                ×
              </button>
            </header>
            <form onSubmit={handleFormSubmit}>
              <div className="form-grid">
                {formFields.map((field) => (
                  <label
                    key={field.key}
                    className={field.kind === 'textarea' ? 'form-wide' : ''}
                  >
                    <span>
                      {field.label}
                      {field.required && <span className="required"> *</span>}
                    </span>
                    {field.kind === 'select' ? (
                      <select
                        name={field.key}
                        defaultValue={editRow ? String(editRow[field.key] ?? '') : ''}
                        required={field.required}
                      >
                        <option value="">Select…</option>
                        {field.options?.map((opt) => (
                          <option key={opt.value} value={opt.value}>
                            {opt.label}
                          </option>
                        ))}
                      </select>
                    ) : field.kind === 'textarea' ? (
                      <textarea
                        name={field.key}
                        defaultValue={editRow ? String(editRow[field.key] ?? '') : ''}
                        required={field.required}
                      />
                    ) : field.kind === 'boolean' ? (
                      <select
                        name={field.key}
                        defaultValue={
                          editRow
                            ? editRow[field.key]
                              ? 'true'
                              : 'false'
                            : 'true'
                        }
                      >
                        <option value="true">Yes</option>
                        <option value="false">No</option>
                      </select>
                    ) : field.kind === 'number' ? (
                      <input
                        type="number"
                        step="any"
                        name={field.key}
                        defaultValue={
                          editRow
                            ? (() => {
                                const v = editRow[field.key];
                                // Many2One → send ID
                                if (
                                  v &&
                                  typeof v === 'object' &&
                                  'id' in v
                                ) {
                                  return (v as Many2One).id;
                                }
                                return v as number;
                              })()
                            : undefined
                        }
                        required={field.required}
                      />
                    ) : (
                      <input
                        type={field.kind === 'date' ? 'date' : 'text'}
                        name={field.key}
                        defaultValue={editRow ? String(editRow[field.key] ?? '') : ''}
                        required={field.required}
                      />
                    )}
                    {field.helper && <small>{field.helper}</small>}
                  </label>
                ))}
              </div>
              <footer>
                <button
                  type="button"
                  className="button button-secondary btn-sm"
                  onClick={() => setFormOpen(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="button button-primary btn-sm"
                  disabled={
                    mutations.create.isPending || mutations.update.isPending
                  }
                >
                  {mutations.create.isPending || mutations.update.isPending
                    ? 'Saving…'
                    : editRow
                      ? 'Update'
                      : 'Create'}
                </button>
              </footer>
            </form>
          </div>
        </div>
      )}

      {/* ─── View detail modal ─── */}
      {viewRow && (
        <div className="modal-backdrop" onClick={() => setViewRow(null)}>
          <div
            className="modal"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
          >
            <header>
              <h2>{String(viewRow.name ?? `Record #${viewRow.id}`)}</h2>
              <button
                className="icon-button"
                onClick={() => setViewRow(null)}
                aria-label="Close"
              >
                ×
              </button>
            </header>
            <div className="detail-grid">
              {fields.map((field) => {
                const value = viewRow[field.key];
                let display: ReactNode;

                if (field.key === 'progress_percentage') {
                  display = <ProgressBar value={Number(value ?? 0)} />;
                } else if (
                  (field.key === statusField || field.key === 'severity') &&
                  value
                ) {
                  const labelKey = `${field.key}_label`;
                  display = (
                    <StatusBadge value={String(value)}>
                      {String(viewRow[labelKey] ?? value)}
                    </StatusBadge>
                  );
                } else {
                  display = formatCell(value, field);
                }

                return (
                  <div key={field.key} className="detail-row">
                    <span className="detail-label">{field.label}</span>
                    <span className="detail-value">{display}</span>
                  </div>
                );
              })}
            </div>
            <footer>
              <button
                className="button button-secondary btn-sm"
                onClick={() => setViewRow(null)}
              >
                Close
              </button>
              <button
                className="button button-primary btn-sm"
                onClick={() => {
                  setEditRow(viewRow);
                  setViewRow(null);
                  setFormOpen(true);
                }}
              >
                Edit
              </button>
            </footer>
          </div>
        </div>
      )}

      {/* ─── Delete confirmation ─── */}
      <ConfirmDialog
        open={deleteId !== null}
        title="Delete record?"
        message="This action cannot be undone. The record will be permanently deleted from the system."
        confirmLabel="Delete"
        danger
        loading={mutations.remove.isPending}
        onConfirm={handleDelete}
        onCancel={() => setDeleteId(null)}
      />
    </div>
  );
}