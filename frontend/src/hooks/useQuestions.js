import { useQuery, useMutation } from '@tanstack/react-query';
import { questionsApi } from '../api/endpoints';

export const useQuestions = (sessionId) => {
    return useQuery({
        queryKey: ['questions', sessionId],
        queryFn: () => questionsApi.fetchAll(sessionId),
        enabled: !!sessionId,
        refetchInterval: 3000,
    });
};

export const usePostQuestion = () => {
    return useMutation({
        mutationFn: (data) => questionsApi.post(data),
    });
};
