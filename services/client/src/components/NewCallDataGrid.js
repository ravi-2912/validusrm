import React from 'react';
import PropTypes from 'prop-types';
import { Container, Row } from 'react-bootstrap';

import DataGrid from './DataGrid';
import { defaultColumnProperties, DateFormatter, currencyFormat } from './helper';

const columns = [
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
    // headerRenderer: () => (
    //   <div>
    //     Undrawn Committment
    //     <br />
    //     before Current
    //     <br />
    //     Drawdown Notice
    //   </div>
    // ),
    formatter: data => <span>${currencyFormat(data.value)}</span>,
  },
  {
    key: 'total_drawdown_notice',
    name: 'Total Drawdown Notice',
    sortable: true,
    filterable: true,
    // headerRenderer: (
    //   <div>
    //     Total
    //     <br />
    //     Drawdown
    //     <br />
    //     Notice
    //   </div>
    // ),
    formatter: data => <span>${currencyFormat(data.value)}</span>,
  },
  {
    key: 'undrawn_committment_after_drawdown',
    name: 'Undrawn Committment after Current Drawdown Notice',
    sortable: true,
    filterable: true,
    width: 240,
    // headerRenderer: (
    //   <div>
    //     Undrawn Committment
    //     <br />
    //     after Current
    //     <br />
    //     Drawdown Notice
    //   </div>
    // ),
    formatter: data => <span>${currencyFormat(data.value)}</span>,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

class NewCallsDataGrid extends React.Component {
  static propTypes = {
    rows: PropTypes.array,
    filters: PropTypes.object,
    onFiltersChange: PropTypes.func,
    onRowsChange: PropTypes.func,
    onAddRow: PropTypes.func,
  };

  render() {
    console.log(this.props.rows);
    return (
      <Container className="my-5 ">
        <Row>
          <h4>Capital Drawdow Calculations</h4>
          <p className="text-left"></p>
          <DataGrid
            columns={columns}
            headerRowHeight={90}
            rows={this.props.rows}
            filters={this.props.filters}
            onFiltersChange={this.props.onFiltersChange}
            onRowsChange={this.props.onRowsChange}
            // onAddRow={this.props.onAddRow}
            // onRowDelete={this.props.onRowDelete}
          />
        </Row>
      </Container>
    );
  }
}

export default NewCallsDataGrid;
