import React from 'react';
import { Container, Row, Button } from 'react-bootstrap';

import DataGrid from './DataGrid';
import { capitalcallsColumns } from './dataGridColumns';

class CapitalCallsDataGrid extends React.Component {
  render() {
    return (
      <Container>
        <Row className="pb-5">
          <h3>Capital Calls</h3>
          <p className="text-left d-block">
            Capital Calls make the final investment from the available funds throught
            First-In-First-Out (FIFO) principle. The calls list show in table below indicates the
            capital call ID, its the date and funds used in the investment to meet the capital
            requirement. The pregress bar indicates only those funds used to meet the capital
            requirements.
          </p>
          <Button href="/newcall">Add a New Call</Button>
        </Row>
        <Row>
          <h4>Capital Calls List</h4>
          <p className="text-left">
            To view confirmed capital calls the list is shown below. The list can be filtered as
            desired. To delete a call press the cross sign, note that this will delete the call and
            funds will be freed. The delete action will not re-allocate the funds to undeleted
            calls.
          </p>
          <DataGrid
            columns={capitalcallsColumns}
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
