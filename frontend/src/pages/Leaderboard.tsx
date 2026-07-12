import { useQuery } from '@tanstack/react-query';
import { getLeaderboard } from '../api/resources.api';
import { Card, EmptyState, ErrorState, LoadingState } from '../components/common';

export default function Leaderboard() {
  const query = useQuery({
    queryKey: ['leaderboard'],
    queryFn: () => getLeaderboard({ limit: 50 }),
  });

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">GAMIFICATION</p>
          <h2>Leaderboard</h2>
          <p className="page-description">
            Employee XP totals from the current company ledger.
          </p>
        </div>
      </div>

      <Card>
        {query.isLoading ? (
          <LoadingState label="Loading leaderboard…" />
        ) : query.error ? (
          <ErrorState
            message={
              query.error instanceof Error
                ? query.error.message
                : 'Unable to load the leaderboard.'
            }
            onRetry={() => query.refetch()}
          />
        ) : query.data && query.data.length > 0 ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th style={{ width: 70 }}>Rank</th>
                  <th>Employee / Dept</th>
                  <th style={{ textAlign: 'right' }}>XP</th>
                </tr>
              </thead>
              <tbody>
                {query.data.map((entry) => (
                  <tr key={entry.rank}>
                    <td>
                      <strong className="rank-number">
                        {entry.rank <= 3 ? ['🥇', '🥈', '🥉'][entry.rank - 1] : `#${entry.rank}`}
                      </strong>
                    </td>
                    <td>{entry.employee?.name ?? 'Unassigned employee'}</td>
                    <td style={{ textAlign: 'right' }}>
                      <b className="xp-value">{entry.xp.toLocaleString()} XP</b>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState
            title="No XP entries"
            detail="The backend returned no leaderboard entries for this company."
          />
        )}
      </Card>
    </>
  );
}
