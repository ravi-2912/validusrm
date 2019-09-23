import React from 'react';
import PropTypes from 'prop-types';
import { Container, Row } from 'react-bootstrap';

import AddFund from './AddFund';
import DataGrid from './DataGrid';
import { ProgressBarFormatter, defaultColumnProperties } from './helper';

import '../css/FundsDataGrid.css';

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
  static propTypes = {
    rows: PropTypes.array,
    filters: PropTypes.object,
    onFiltersChange: PropTypes.func,
    onRowsChange: PropTypes.func,
    onAddRow: PropTypes.func,
    onRowDelete: PropTypes.func,
    addFundToDB: PropTypes.func,
  };

  render() {
    return (
      <Container>
        <Row className="main-desc">
          <h3>Funds Management</h3>
          <p className="desc">
            Manage funds by adding more or deleting. For deleting funds thast have committments or
            invested these need to be deleted first. The table below list all funds. The progress
            bar indicated the total investment / total committed for the fund.
          </p>
          <AddFund addToDB={this.props.addFundToDB} />
        </Row>
        <Row>
          <h4>Funds List</h4>
          <p className="desc">
            To filter press the Filter button. To edit fund name double click the fund name cell and
            edit, once done press enter and it will autpomatically post the data in the database. To
            delete the fund presse the cross sign.
          </p>
          <DataGrid
            columns={columns}
            rows={this.props.rows}
            filters={this.props.filters}
            onFiltersChange={this.props.onFiltersChange}
            onRowsChange={this.props.onRowsChange}
            onAddRow={this.props.onAddRow}
            onRowDelete={this.props.onRowDelete}
          />
        </Row>
      </Container>
    );
  }
}

export default FundsDataGrid;
