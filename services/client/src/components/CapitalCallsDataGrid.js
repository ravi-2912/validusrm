import React from 'react';
import { Container, Row, Button } from 'react-bootstrap';

import DataGrid from './DataGrid';
import CallsProgressBar from './CallProgressBar';
import { defaultColumnProperties, DateFormatter, currencyFormat } from './helper';

const columns = [
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
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 80,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

class CapitalCallsDataGrid extends React.Component {
  render() {
    return (
      <Container>
        <Row className="pb-5">
          <h3>Capital Calls</h3>
          <p className="text-left d-block">To add a new capital call press the button below.</p>
          <Button href="/newcall">Add a New Call</Button>
        </Row>
        <Row>
          <h4>Capital Calls List</h4>
          <p className="text-left">
            To view confirmed capital calls the list is shown below. The list can be filtered as
            desired. In the list, the capital required are fullfilled from various funds.
          </p>
          <DataGrid
            columns={columns}
            rows={this.props.rows}
            filters={this.props.filters}
            onFiltersChange={this.props.onFiltersChange}
            onRowsChange={this.props.onRowsChange}
            onRowDelete={this.props.onRowDelete}
          />
        </Row>
      </Container>
    );
  }
}

export default CapitalCallsDataGrid;
