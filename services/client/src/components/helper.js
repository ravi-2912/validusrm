import React from 'react';
import { ProgressBar } from 'react-bootstrap';

export const ProgressBarFormatter = data => {
  const value = data.value.value;
  const totalInvested = data.value.totalInvested;
  const totalCommitted = data.value.totalCommitted;
  return (
    <div>
      <ProgressBar striped now={value} label={`$ ${totalInvested} / $ ${totalCommitted}`} />
    </div>
  );
};

export const defaultColumnProperties = {
  resizable: true,
};

export const DateFormatter = date => {
  const dateString = date.value.toString().split(' ')[0];

  return <div>{dateString}</div>;
};
