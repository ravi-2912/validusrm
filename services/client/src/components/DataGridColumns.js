import React from 'react';

import { currencyFormat } from './helper';
import FundProgressBar from './FundProgressBar';
import CallsProgressBar from './CallProgressBar';

export const defaultColumnProperties = {
  resizable: true,
};

export const DateFormatter = date => {
  const dateString = date.value.toString().split(' ')[0];

  return <div>{dateString}</div>;
};

export const fundsColumns = [
  {
    key: 'id',
    name: 'ID',
    sortDescendingFirst: true,
    sortable: true,
    width: 80,
    filterable: true,
  },
  {
    key: 'name',
    name: 'Fund Name',
    editable: true,
    sortable: true,
    width: 180,
    filterable: true,
  },
  {
    key: 'invested_committed',
    name: 'Total Invested / Total Committed',
    sortable: true,
    formatter: FundProgressBar,
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 80,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

export const committmentsColumns = [
  {
    key: 'id',
    name: 'ID',
    sortDescendingFirst: true,
    sortable: true,
    width: 80,
    filterable: true,
  },
  {
    key: 'fund_id',
    name: 'Fund ID',
    editable: true,
    sortable: true,
    width: 120,
    filterable: true,
  },
  {
    key: 'amount',
    name: 'Amount',
    editable: true,
    sortable: true,
    width: 120,
    filterable: true,
    formatter: data => {
      return <span>${currencyFormat(data.value)}</span>;
    },
  },
  {
    key: 'date',
    name: 'Date',
    editable: true,
    sortable: true,
    width: 120,
    filterable: true,
    formatter: DateFormatter,
  },
  {
    key: 'invested_committed',
    name: 'Total Invested / Committed Amount',
    sortable: true,
    formatter: FundProgressBar,
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 80,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

export const capitalcallsColumns = [
  {
    key: 'date',
    name: 'Date',
    sortDescendingFirst: true,
    sortable: true,
    width: 120,
    filterable: true,
    formatter: DateFormatter,
  },
  {
    key: 'id',
    name: 'Call ID',
    sortable: true,
    width: 90,
    filterable: true,
  },
  {
    key: 'capital',
    name: 'Capital',
    sortable: true,
    width: 90,
    filterable: true,
    formatter: data => {
      return <span>${currencyFormat(data.value)}</span>;
    },
  },
  {
    key: 'investment_breakdown',
    name: 'Investments Breakdown',
    formatter: CallsProgressBar,
    sortable: true,
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 80,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

export const newcallColumns = [
  {
    key: 'id',
    name: 'ID',
    sortDescendingFirst: true,
    sortable: true,
    width: 60,
    filterable: true,
  },
  {
    key: 'fund_name',
    name: 'Fund',
    sortable: true,
    width: 120,
    filterable: true,
    formatter: data => <div>{data.row.fund_name}</div>,
  },
  {
    key: 'date',
    name: 'Date',
    sortable: true,
    width: 120,
    filterable: true,
    formatter: DateFormatter,
  },
  {
    key: 'amount',
    name: 'Committment',
    sortable: true,
    width: 140,
    filterable: true,
    formatter: data => <span>${currencyFormat(data.value)}</span>,
  },
  {
    key: 'undrawn_committment_before_drawdown',
    name: 'Undrawn Committment before Current Drawdown Notice',
    sortable: true,
    filterable: true,
    width: 240,
    headerRenderer: (
      <div>
        Undrawn Committment
        <br />
        Before Current
        <br />
        Drawdown Notice
      </div>
    ),
    formatter: data => <span>${currencyFormat(data.value)}</span>,
  },
  {
    key: 'total_drawdown_notice',
    name: 'Total Drawdown Notice',
    sortable: true,
    filterable: true,
    headerRenderer: (
      <div>
        Total
        <br />
        Drawdown
        <br />
        Notice
      </div>
    ),
    formatter: data => <span>${currencyFormat(data.value)}</span>,
  },
  {
    key: 'undrawn_committment_after_drawdown',
    name: 'Undrawn Committment after Current Drawdown Notice',
    sortable: true,
    filterable: true,
    width: 240,
    headerRenderer: (
      <div>
        Undrawn Committment
        <br />
        After Current
        <br />
        Drawdown Notice
      </div>
    ),
    formatter: data => <span>${currencyFormat(data.value)}</span>,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));
