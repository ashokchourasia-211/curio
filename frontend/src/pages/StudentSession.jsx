import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useSessionDetails } from '../hooks/useSession';
import { useQuestions, usePostQuestion } from '../hooks/useQuestions';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Send } from 'lucide-react';

export default function StudentSession() {
    const { code } = useParams();
    const [questionText, setQuestionText] = useState('');
    const [studentHash] = useState(() => {
        let hash = localStorage.getItem('curio_student_hash');
        if (!hash) {
            hash = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('curio_student_hash', hash);
        }
        return hash;
    });
    const [error, setError] = useState('');

    // 1. Session Details
    const { data: sessionData, isLoading: isSessionLoading } = useSessionDetails(code);
    const verifyData = sessionData || {};
    const sessionId = verifyData.session_id;

    // 2. Poll Questions
    const { data: questions } = useQuestions(sessionId);

    // 3. Post Question Mutation
    const postQuestion = usePostQuestion();

    const handleSend = async (e) => {
        e.preventDefault();
        if (!questionText.trim()) return;
        if (!sessionId) return;

        setError('');

        try {
            await postQuestion.mutateAsync({
                session_id: sessionId,
                text: questionText,
                student_hash: studentHash
            });
            setQuestionText('');
            // Scroll to bottom?
        } catch (err) {
            console.error("Failed to post question:", err);
            setError('Failed to send question. Please try again.');
        }
    };

    if (isSessionLoading) return <div className="p-8 text-center">Entering classroom...</div>;
    if (!verifyData.valid) return <div className="p-8 text-center text-red-500">Invalid Session</div>;

    return (
        <div className="flex flex-col h-screen bg-background text-foreground">
            {/* Header */}
            <header className="p-4 border-b bg-card shadow-sm sticky top-0 z-10">
                <div className="max-w-3xl mx-auto flex justify-between items-center">
                    <div>
                        <h1 className="text-xl font-bold">{verifyData.subject}</h1>
                        <p className="text-xs text-muted-foreground">Anonymous Classroom ({code})</p>
                    </div>
                    <Badge variant="outline" className="text-xs">
                        ID: {studentHash.substr(0, 6)}...
                    </Badge>
                </div>
            </header>

            {/* Feed */}
            <main className="flex-1 overflow-y-auto p-4 pb-24">
                <div className="max-w-3xl mx-auto space-y-4">
                    {questions && questions.length > 0 ? (
                        questions.map((q) => (
                            <Card key={q.question_id} className={q.student_hash === studentHash ? "border-primary" : ""}>
                                <CardHeader className="pb-2 p-4">
                                    <div className="flex justify-between items-start">
                                        <span className={`text-sm font-semibold ${q.student_hash === studentHash ? "text-primary" : "text-muted-foreground"}`}>
                                            {q.student_hash === studentHash ? "You" : q.student_name}
                                        </span>
                                        <span className="text-[10px] text-muted-foreground">{new Date(q.created_at).toLocaleTimeString()}</span>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-4 pt-0">
                                    <p className="mb-2">{q.text}</p>
                                    {q.status === 'flagged' ? (
                                        <Badge variant="destructive" className="text-[10px]">Message Flagged</Badge>
                                    ) : (
                                        <div className="bg-secondary/50 p-3 rounded text-sm">
                                            <span className="font-bold text-primary text-xs uppercase block mb-1">AI Answer</span>
                                            {q.ai_response}
                                        </div>
                                    )}
                                </CardContent>
                            </Card>
                        ))
                    ) : (
                        <div className="text-center text-muted-foreground py-20">
                            <p>No questions yet.</p>
                            <p className="text-sm">Be the first to ask!</p>
                        </div>
                    )}
                </div>
            </main>

            {/* Input Area */}
            <footer className="p-4 bg-background border-t fixed bottom-0 left-0 right-0">
                <div className="max-w-3xl mx-auto">
                    {error && <p className="text-xs text-red-500 mb-2">{error}</p>}
                    <form onSubmit={handleSend} className="flex gap-2">
                        <Input
                            placeholder="Type your doubt here..."
                            value={questionText}
                            onChange={(e) => setQuestionText(e.target.value)}
                            className="flex-1"
                            autoComplete="off"
                        />
                        <Button type="submit" size="icon" disabled={postQuestion.isPending || !questionText.trim()}>
                            <Send className="h-4 w-4" />
                        </Button>
                    </form>
                </div>
            </footer>
        </div>
    );
}
