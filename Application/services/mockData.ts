export type CallRecord = {
  id: string;
  caller: string;
  intent: 'Support' | 'Sales' | 'Billing' | 'Demo';
  duration: number;
  time: string;
  status: 'Completed' | 'Transferred' | 'Missed' | 'Voicemail';
  transcription: string;
};

export const callMetrics = {
  callsToday: 210,
  totalMinutes: 1840,
  successRate: 92,
  activeAgents: 24,
  trend: {
    callsToday: 13,
    totalMinutes: 8,
    successRate: 5,
    activeAgents: 2
  }
};

export const liveCalls = [
  { id: 'C-3032', caller: '+1 555-0198', agent: 'Ana K.', intent: 'Support', duration: '00:07:31' },
  { id: 'C-3041', caller: '+44 20 7946 0958', agent: 'Jonas L.', intent: 'Sales', duration: '00:02:19' },
  { id: 'C-3638', caller: '+1 615-445-0162', agent: 'Maya N.', intent: 'Billing', duration: '00:12:30' }
];

export const callLogs: CallRecord[] = Array.from({ length: 45 }, (_, i) => {
  const intents: CallRecord['intent'][] = ['Support', 'Sales', 'Billing', 'Demo'];
  const statuses: CallRecord['status'][] = ['Completed', 'Transferred', 'Missed', 'Voicemail'];
  const intent = intents[i % intents.length];
  const status = statuses[i % statuses.length];
  return {
    id: `CL-${5000 + i}`,
    caller: `+1 800 555 ${String(1000 + i).padStart(4, '0')}`,
    intent,
    duration: Math.floor(Math.random() * 25) + 1,
    time: `2025-11-${(i % 30 + 1).toString().padStart(2, '0')} 0${(i % 9) + 8}:00`,
    status,
    transcription:
      "(AI Agent) Hello, this is Breezi. How can I assist you today? ... (customer response, etc)"
  };
});

export const analyticsData = {
  volume: [
    { day: 'Mon', calls: 120 },
    { day: 'Tue', calls: 145 },
    { day: 'Wed', calls: 172 },
    { day: 'Thu', calls: 158 },
    { day: 'Fri', calls: 186 },
    { day: 'Sat', calls: 93 },
    { day: 'Sun', calls: 79 }
  ],
  successRate: [
    { day: 'Mon', rate: 88 },
    { day: 'Tue', rate: 92 },
    { day: 'Wed', rate: 90 },
    { day: 'Thu', rate: 93 },
    { day: 'Fri', rate: 96 }
  ],
  intentDist: [
    { name: 'Support', value: 42 },
    { name: 'Sales', value: 32 },
    { name: 'Billing', value: 18 },
    { name: 'Demo', value: 8 }
  ]
};
