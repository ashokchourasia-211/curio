import { useParams } from 'react-router-dom';
import { useSessionDetails } from '../hooks/useSession';
import { useQuestions } from '../hooks/useQuestions';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default function TeacherMonitor() {
    const { code } = useParams();
    const { data: sessionData, isLoading: isSessionLoading } = useSessionDetails(code);

    const verifyData = sessionData || {};
    const sessionId = verifyData.session_id;

    // Only poll if we have a valid session ID
    const { data: questions } = useQuestions(sessionId);

    if (isSessionLoading) return <div className="p-8 text-center">Loading session...</div>;
    if (!verifyData.valid) return <div className="p-8 text-center text-red-500">Invalid Session Code</div>;

    return (
        <div className="min-h-screen bg-background text-foreground p-8">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold">{verifyData.subject || 'Classroom'}</h1>
                    <p className="text-muted-foreground">Monitor View</p>
                </div>
                <Card className="bg-primary text-primary-foreground">
                    <CardContent className="p-4 flex flex-col items-center justify-center">
                        <p className="text-sm font-medium uppercase opacity-80">Session Code</p>
                        <p className="text-4xl font-black tracking-widest">{code}</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {questions && questions.length > 0 ? (
                    questions.map((q) => (
                        <Card key={q.question_id} className={q.status === 'flagged' ? "border-red-500 border-2" : ""}>
                            <CardHeader className="pb-2">
                                <div className="flex justify-between items-start">
                                    <CardTitle className="text-lg">{q.student_name}</CardTitle>
                                    <span className="text-xs text-muted-foreground">{new Date(q.created_at).toLocaleTimeString()}</span>
                                </div>
                            </CardHeader>
                            <CardContent>
                                <p className="font-medium mb-3 text-lg">{q.text}</p>
                                {q.status === 'flagged' ? (
                                    <Badge variant="destructive">Toxic / Flagged</Badge>
                                ) : (
                                    <div className="bg-muted p-3 rounded-md text-sm border-l-4 border-primary">
                                        <span className="font-bold text-primary block mb-1">AI Answer:</span>
                                        {q.ai_response}
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <div className="col-span-full text-center text-muted-foreground py-12 bg-muted/20 rounded-lg border border-dashed">
                        <p className="text-lg">No questions yet.</p>
                        <p className="text-sm">Students can join using code <strong>{code}</strong></p>
                    </div>
                )}
            </div>
        </div>
    );
}
