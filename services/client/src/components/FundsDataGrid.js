import React from 'react';
import DataGrid from './DataGrid';
import { Container, Row } from 'react-bootstrap';
import { ProgressBarFormatter, defaultColumnProperties } from './helper';

const columns = [
  {
    key: 'id',
    name: 'ID',
    sortDescendingFirst: true,
    sortable: true,
    width: 120,
  },
  {
    key: 'name',
    name: 'Fund Name',
    editable: true,
    sortable: true,
    width: 250,
  },
  {
    key: 'invested_committed',
    name: 'Total Invested & Committed',
    sortable: true,
    formatter: ProgressBarFormatter,
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 120,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

class FundsDataGrid extends React.Component {
  render() {
    return (
      <Container>
        <Row>
          <DataGrid
            rows={this.props.funds}
            columns={columns}
            filters={this.props.filters}
            onFiltersChange={this.props.onFiltersChange}
            onRowsChange={this.props.onRowsChange}
          />
        </Row>
      </Container>
    );
  }
}

export default FundsDataGrid;
