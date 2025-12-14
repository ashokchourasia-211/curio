import { useMutation, useQuery } from '@tanstack/react-query';
import { sessionsApi } from '../api/endpoints';

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
