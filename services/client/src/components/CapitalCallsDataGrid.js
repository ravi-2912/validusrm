import React from 'react';
import DataGrid from './DataGrid';
import { Container, Row, Col, ProgressBar } from 'react-bootstrap';

import FundsProgressBar from './FundProgressBar';
import { defaultColumnProperties, DateFormatter } from './helper';
import '../css/CapitalCallsDataGrid.css';

const ProgBarFormatter = data => {
  console.log('DATA', data.row);
  const fics = data.row.fund_invested_committed;
  console.log('FICS', fics);
  return (
    <Row>
      {fics.map((fic, ind) => (
        <Col key={ind}>
          <FundsProgressBar value={fic} />
        </Col>
      ))}
    </Row>
  );
};

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
    width: 100,
    filterable: true,
  },
  // {
  //   key: 'name',
  //   name: 'Investment Name',
  //   editable: true,
  //   sortable: true,
  //   width: 180,
  //   filterable: true,
  // },
  {
    key: 'investment_breakdown',
    name: 'Investments',
    formatter: ProgBarFormatter,
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
        {/* <Row className="main-desc">
          <h3>Capital Calls</h3>
          <p className="desc">
            Manage committments by adding more or deleting. For deleting committments that have are
            inveseted these need to be deleted first. The table below list all committments. The
            progress bar indicated the total investment / total committed for the committment.
          </p>
          <AddCommittment addToDB={this.props.addCommittmentToDB} funds={this.props.funds} />
        </Row> */}
        <Row>
          {/* <h4>Capital Calls List</h4>
          <p className="desc">
            To filter press the Filter button. To edit committment name double click the committment
            name cell and edit, once done press enter and it will autpomatically post the data in
            the database. To delete the committment presse the cross sign.
          </p> */}
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
