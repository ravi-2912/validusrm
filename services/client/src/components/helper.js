import React from 'react';
import { ProgressBar } from 'react-bootstrap';

export const ProgressBarFormatter = data => {
  console.log(data);
  const value = data.value.value;
  const totalInvested = data.value.totalInvested;
  const totalCommitted = data.value.totalCommitted;
  return <ProgressBar now={value} label={`$ ${totalInvested} / $ ${totalCommitted}`} />;
};

export const defaultColumnProperties = {
  resizable: true,
  filterable: true,
};
