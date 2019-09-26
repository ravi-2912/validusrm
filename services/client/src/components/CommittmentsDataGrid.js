import React from 'react';
import DataGrid from './DataGrid';
import AddCommittment from './AddCommittment';
import { Container, Row } from 'react-bootstrap';
import { defaultColumnProperties, DateFormatter } from './helper';
import FundsProgressBar from './FundProgressBar';

const columns = [
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
  },
  {
    key: 'date',
    name: 'Date',
    editable: true,
    sortable: true,
    width: 200,
    filterable: true,
    formatter: DateFormatter,
  },
  {
    key: 'invested_committed',
    name: 'Total Invested & Committed',
    sortable: true,
    formatter: FundsProgressBar,
  },
  {
    key: 'actions',
    name: 'Actions',
    width: 120,
  },
].map(c => ({ ...c, ...defaultColumnProperties }));

class CommittmentsDataGrid extends React.Component {
  render() {
    return (
      <Container>
        <Row className="main-desc">
          <h3>Committments Management</h3>
          <p className="desc">
            Manage committments by adding more or deleting. For deleting committments that have are
            inveseted these need to be deleted first. The table below list all committments. The
            progress bar indicated the total investment / total committed for the committment.
          </p>
          <AddCommittment addToDB={this.props.addCommittmentToDB} funds={this.props.funds} />
        </Row>
        <Row>
          <h4>Committments List</h4>
          <p className="desc">
            To filter press the Filter button. To edit committment name double click the committment
            name cell and edit, once done press enter and it will autpomatically post the data in
            the database. To delete the committment presse the cross sign.
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

export default CommittmentsDataGrid;
