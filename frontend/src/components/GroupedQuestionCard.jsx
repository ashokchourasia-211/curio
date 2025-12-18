import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAnswerGroup } from '../hooks/useSession';

export default function GroupedQuestionCard({ group }) {
  const [answer, setAnswer] = useState('');
  const answerGroup = useAnswerGroup();

  const handleAnswer = async (e) => {
    e.preventDefault();
    if (!answer.trim()) return;

    try {
      await answerGroup.mutateAsync({
        groupId: group.id,
        answer: answer,
      });
      setAnswer('');
    } catch (error) {
      console.error('Failed to answer group:', error);
    }
  };

  return (
    <Card className="border-l-4 border-indigo-500 shadow-md">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardTitle className="text-lg font-bold text-indigo-700">
            {group.topic || 'Grouped Questions'}
          </CardTitle>
          <Badge variant="secondary" className="bg-indigo-100 text-indigo-700">
            {group.question_count} Questions
          </Badge>
        </div>
        <p className="text-xs text-muted-foreground">
          Created at {new Date(group.created_at).toLocaleTimeString()}
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <p className="text-sm text-gray-600">
            Similar questions grouped together. Answering this will update all
            of them.
          </p>

          <form onSubmit={handleAnswer} className="flex gap-2">
            <Input
              placeholder="Answer for everyone..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              disabled={answerGroup.isPending}
            />
            <Button
              type="submit"
              size="sm"
              disabled={answerGroup.isPending || !answer.trim()}
            >
              {answerGroup.isPending ? 'Sent' : 'Send'}
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  );
}
