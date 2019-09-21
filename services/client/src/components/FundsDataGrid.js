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
    filterable: true,
  },
  {
    key: 'name',
    name: 'Fund Name',
    editable: true,
    sortable: true,
    width: 250,
    filterable: true,
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
            columns={columns}
            rows={this.props.rows}
            filters={this.props.filters}
            onFiltersChange={this.props.onFiltersChange}
            onRowsChange={this.props.onRowsChange}
            onAddRow={this.props.onAddRow}
          />
        </Row>
      </Container>
    );
  }
}

export default FundsDataGrid;
