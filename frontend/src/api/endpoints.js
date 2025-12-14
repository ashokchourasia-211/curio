import { apiClient } from './client';

export const sessionsApi = {
    create: async (data) => {
        const response = await apiClient.post('/sessions', data);
        return response.data;
    },
    verify: async (code) => {
        const response = await apiClient.get(`/sessions/verify/${code}`);
        return response.data;
    },
};

export const questionsApi = {
    post: async (data) => {
        const response = await apiClient.post('/questions', data);
        return response.data;
    },
    fetchAll: async (sessionId, lastSeenTimestamp) => {
        const params = lastSeenTimestamp ? { last_seen_timestamp: lastSeenTimestamp } : {};
        const response = await apiClient.get(`/questions/${sessionId}`, { params });
        return response.data;
    },
};
