import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateSession } from '../hooks/useSession';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

export default function TeacherDashboard() {
    const [subject, setSubject] = useState('');
    const [teacherId, setTeacherId] = useState('teacher_001');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const createSession = useCreateSession();

    const handleCreate = async (e) => {
        e.preventDefault();
        if (!subject || !teacherId) return;

        setError('');

        try {
            const response = await createSession.mutateAsync({
                teacher_id: teacherId,
                subject: subject
            });
            if (response && response.code) {
                navigate(`/monitor/${response.code}`);
            } else {
                setError('Failed to create session.');
            }
        } catch (err) {
            console.error("Create session failed:", err);
            setError('Failed to create session. Please try again.');
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-background text-foreground p-4">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl text-center">Teacher Dashboard</CardTitle>
                    <CardDescription className="text-center">Create a new classroom session</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleCreate} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="teacherId">Teacher ID</Label>
                            <Input
                                id="teacherId"
                                placeholder="teacher_001"
                                value={teacherId}
                                onChange={(e) => setTeacherId(e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="subject">Subject</Label>
                            <Input
                                id="subject"
                                placeholder="e.g. Physics 101"
                                value={subject}
                                onChange={(e) => setSubject(e.target.value)}
                            />
                        </div>
                        {error && <p className="text-sm text-red-500 text-center">{error}</p>}
                        <Button type="submit" className="w-full" disabled={createSession.isPending}>
                            {createSession.isPending ? 'Creating...' : 'Start Session'}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
