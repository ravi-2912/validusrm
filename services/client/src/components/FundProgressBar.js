import React from 'react';
import { ProgressBar } from 'react-bootstrap';
import { currencyFormat } from './helper';

function FundProgressBar(props) {
  const fund_name = props.value.fund_name;
  const value = props.value.value;
  const totalInvested = currencyFormat(props.value.totalInvested);
  const totalCommitted = currencyFormat(props.value.totalCommitted);
  let label_1 = fund_name !== '' ? `${fund_name}: ` : '';
  let label = `${label_1}$${totalInvested} / $${totalCommitted}`;
  return (
    <div>
      <ProgressBar striped now={value} label={label} />
    </div>
  );
}

export default FundProgressBar;
