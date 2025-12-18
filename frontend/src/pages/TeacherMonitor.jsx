import { useParams } from 'react-router-dom';
import { useSessionDetails, useGroups } from '../hooks/useSession';
import { useQuestions } from '../hooks/useQuestions';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import GroupedQuestionCard from '@/components/GroupedQuestionCard';

export default function TeacherMonitor() {
  const { code } = useParams();
  const { data: sessionData, isLoading: isSessionLoading } =
    useSessionDetails(code);

  const verifyData = sessionData || {};
  const sessionId = verifyData.session_id;

  // Poll for questions and groups
  const { data: questions } = useQuestions(sessionId);
  const { data: groups } = useGroups(sessionId);

  if (isSessionLoading)
    return <div className="p-8 text-center">Loading session...</div>;
  if (!verifyData.valid)
    return (
      <div className="p-8 text-center text-red-500">Invalid Session Code</div>
    );

  // Filter out grouped questions from the main list so they don't appear twice?
  // Actually, per plan, maybe we show them in both places or just highlight.
  // For now, let's show ALL individual questions on left, and Groups on right.
  // Ideally, we might want to hide questions that are part of a group from the main stream,
  // but the API doesn't give us that info easily yet without iterating.
  // Let's keep it simple: Two streams.

  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">
            {verifyData.subject || 'Classroom'}
          </h1>
          <p className="text-muted-foreground">Monitor View</p>
        </div>
        <Card className="bg-primary text-primary-foreground">
          <CardContent className="p-4 flex flex-col items-center justify-center">
            <p className="text-sm font-medium uppercase opacity-80">
              Session Code
            </p>
            <p className="text-4xl font-black tracking-widest">{code}</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Live Stream (2/3 width) */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-xl font-semibold mb-4">Live Questions</h2>
          {questions && questions.length > 0 ? (
            questions.map((q) => (
              <Card
                key={q.question_id}
                className={
                  q.status === 'flagged' ? 'border-red-500 border-2' : ''
                }
              >
                <CardHeader className="pb-2">
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg">{q.student_name}</CardTitle>
                    <span className="text-xs text-muted-foreground">
                      {new Date(q.created_at).toLocaleTimeString()}
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="font-medium mb-3 text-lg">{q.text}</p>
                  {q.status === 'flagged' ? (
                    <Badge variant="destructive">Toxic / Flagged</Badge>
                  ) : (
                    <div className="bg-muted p-3 rounded-md text-sm border-l-4 border-primary">
                      <span className="font-bold text-primary block mb-1">
                        AI Answer:
                      </span>
                      {q.ai_response || 'Processing...'}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="text-center text-muted-foreground py-12 bg-muted/20 rounded-lg border border-dashed">
              <p>No questions yet.</p>
            </div>
          )}
        </div>

        {/* Right Column: Smart Groups (1/3 width) */}
        <div className="space-y-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Smart Groups</h2>
            <Badge
              variant="outline"
              className="animate-pulse text-indigo-600 border-indigo-200"
            >
              AI Active
            </Badge>
          </div>

          {groups && groups.length > 0 ? (
            groups.map((group) => (
              <GroupedQuestionCard key={group.id} group={group} />
            ))
          ) : (
            <div className="text-center text-muted-foreground py-12 bg-indigo-50/50 rounded-lg border border-dashed border-indigo-100">
              <p className="text-sm">Waiting for similar questions...</p>
              <p className="text-xs mt-1">AI will group them here.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
