import React from 'react';
import type { LeadStatus, QualificationScore } from '../types';

interface StatusDotProps {
  status?: LeadStatus | QualificationScore | string;
  label?: string;
}

export const StatusDot: React.FC<StatusDotProps> = ({ status, label }) => {
  const s = (status || '').toLowerCase();
  
  let dotColor = 'bg-gray-400';
  let textColor = 'text-gray-700';
  let bgBadge = 'bg-gray-50';

  if (s === 'hot') {
    dotColor = 'bg-red-500';
    textColor = 'text-red-700';
    bgBadge = 'bg-red-50';
  } else if (s === 'warm') {
    dotColor = 'bg-amber-500';
    textColor = 'text-amber-700';
    bgBadge = 'bg-amber-50';
  } else if (s === 'cold') {
    dotColor = 'bg-blue-500';
    textColor = 'text-blue-700';
    bgBadge = 'bg-blue-50';
  } else if (s === 'new' || s === 'follow_up') {
    dotColor = 'bg-purple-500';
    textColor = 'text-purple-700';
    bgBadge = 'bg-purple-50';
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${bgBadge} ${textColor}`}>
      <span className={`w-2 h-2 rounded-full ${dotColor} mr-1.5 animate-pulse`} />
      {label || s.toUpperCase()}
    </span>
  );
};
