import React from 'react';
import * as Numeral from 'numeral';
import { ProgressBar } from 'react-bootstrap';

export const currencyFormat = val => {
  let cur = Numeral(val).format('0.00a');
  const curSplitted = cur.split('.');
  const dec = curSplitted[1].slice(0, 2);
  if (dec === '00') {
    cur = curSplitted[0] + curSplitted[1].slice(2);
  }
  return cur;
};

export const defaultColumnProperties = {
  resizable: true,
};

export const DateFormatter = date => {
  const dateString = date.value.toString().split(' ')[0];

  return <div>{dateString}</div>;
};

export const calcs_for_funds_invested_committed = (committments, fund = undefined) => {
  let totalCommitted = 0;
  let totalInvested = 0;
  for (let c of committments) {
    totalCommitted += c.amount;
    for (let i of c.investments) {
      totalInvested += i.investment;
    }
  }
  // added this for progressbar values
  const invested_committed = {
    fund_id: fund ? fund.id : 0,
    fund_name: fund ? fund.name : '',
    value: totalCommitted === 0 ? 0 : (100 * totalInvested) / totalCommitted,
    totalCommitted: totalCommitted,
    totalInvested: totalInvested,
  };
  return invested_committed;
};
