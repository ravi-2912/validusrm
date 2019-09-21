import React from 'react';
import { ProgressBar } from 'react-bootstrap';

export const ProgressBarFormatter = ({ value }) => {
  return <ProgressBar now={value} label={`${value}%`} />;
};

export const defaultColumnProperties = {
  resizable: true,
  filterable: true,
};
