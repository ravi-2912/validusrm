import React from 'react';
import DataGrid from './DataGrid';
import AddCommittment from './AddCommittment';
import { Container, Row } from 'react-bootstrap';
import { committmentsColumns } from './DataGridColumns';

class CommittmentsDataGrid extends React.Component {
  render() {
    return (
      <Container>
        <Row className="pb-5">
          <h3>Committments Management</h3>
          <p className="text-left">
            Manage committments by adding more or deleting. For deleting committments that have are
            inveseted these need to be deleted first. The table below list all committments. The
            progress bar indicated the total investment / total committed for the committment.
          </p>
          <AddCommittment addToDB={this.props.addCommittmentToDB} funds={this.props.funds} />
        </Row>
        <Row>
          <h4>Committments List</h4>
          <p className="text-left">
            To filter press the Filter button. To edit committment name double click the committment
            name cell and edit, once done press enter and it will autpomatically post the data in
            the database. To delete the committment presse the cross sign.
          </p>
          <DataGrid
            columns={committmentsColumns}
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
