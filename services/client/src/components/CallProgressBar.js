import React from 'react';
import { ProgressBar } from 'react-bootstrap';
import { currencyFormat } from './helper';

function CallsProgressBar(props) {
  const capital = props.row.capital;
  const invs = props.row.investments;
  const colors = ['success', 'danger', 'warning', 'info'];

  return (
    <ProgressBar>
      {invs.map((inv, ind) => {
        const amount = currencyFormat(inv.investment);
        const label = `${inv.fund_name}: $${amount}`;
        let now = (100 * inv.investment) / capital;
        return (
          <ProgressBar
            key={ind}
            // className={now < 15 ? "w-25" : ""}
            label={label}
            now={now < 20 ? 20 : now}
            variant={colors[ind % colors.length]}
            striped
          />
        );
      })}
    </ProgressBar>
  );
}
export default CallsProgressBar;
