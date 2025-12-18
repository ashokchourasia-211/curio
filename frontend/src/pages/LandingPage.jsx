import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useVerifySession } from '../hooks/useSession';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardDescription,
} from '@/components/ui/card';
import { Label } from '@/components/ui/label';

export default function LandingPage() {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const verifySession = useVerifySession();

  const handleJoin = async (e) => {
    e.preventDefault();
    if (!code) return;

    setError('');

    try {
      const response = await verifySession.mutateAsync(code);
      if (response && response.valid) {
        navigate(`/session/${code}`);
      } else {
        setError('Invalid session code.');
      }
    } catch (err) {
      console.error('Join failed:', err);
      setError('Failed to join session. Please try again.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background text-foreground p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-2xl text-center">Curio</CardTitle>
          <CardDescription className="text-center">
            Anonymous Classroom Q&A
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleJoin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="code">Session Code</Label>
              <Input
                id="code"
                placeholder="e.g. PHY-88"
                value={code}
                onChange={(e) => setCode(e.target.value.toUpperCase())}
                className="text-center text-lg uppercase tracking-widest"
              />
            </div>
            {error && (
              <p className="text-sm text-red-500 text-center">{error}</p>
            )}
            <Button
              type="submit"
              className="w-full"
              disabled={verifySession.isPending}
            >
              {verifySession.isPending ? 'Joining...' : 'Join Class'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
