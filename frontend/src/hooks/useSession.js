import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { sessionsApi, groupsApi } from '../api/endpoints';

export const useCreateSession = () => {
  return useMutation({
    mutationFn: (data) => sessionsApi.create(data),
  });
};

export const useVerifySession = () => {
  return useMutation({
    mutationFn: (code) => sessionsApi.verify(code),
  });
};

export const useSessionDetails = (code) => {
  return useQuery({
    queryKey: ['session', code],
    queryFn: () => sessionsApi.verify(code),
    enabled: !!code,
    retry: false,
  });
};

export const useGroups = (sessionId) => {
  return useQuery({
    queryKey: ['groups', sessionId],
    queryFn: () => groupsApi.getSessionGroups(sessionId),
    enabled: !!sessionId,
    refetchInterval: 3000, // Poll every 3 seconds
  });
};

export const useAnswerGroup = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ groupId, answer }) => groupsApi.answerGroup(groupId, answer),
    onSuccess: () => {
      // Invalidate groups and questions to refresh UI
      queryClient.invalidateQueries({ queryKey: ['groups'] });
      // Ideally we also invalidate specific session questions but we might not have sessionId handy in mutation
      queryClient.invalidateQueries({ queryKey: ['questions'] });
    },
  });
};
