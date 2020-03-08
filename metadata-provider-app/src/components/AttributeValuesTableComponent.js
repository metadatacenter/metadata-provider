import React from 'react';
import Table from "react-bootstrap/Table";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import SampleDetailsModal from "./SampleDetailsModal";
import ProjectDetailsModal from "./ProjectDetailsModal";

export default function ResultsTableComponent(props) {


  return (
    <>
      {props.attributeValuesAggMap && Object.keys(props.attributeValuesAggMap).length > 0 &&
      <Container>
        <Row>
          <Col>
            <Container>
              <div className="results">
                <Table size={'sm'} striped bordered hover variant="dark">
                  <thead>
                  <tr>
                    <th>#</th>
                    <th>{props.content}</th>
                    <th>No. samples</th>
                  </tr>
                  </thead>
                  <tbody>
                  {Object.keys(props.attributeValuesAggMap).map((key, index) => (
                    <tr key={key}>
                      <td>{index + 1}</td>
                      <td>{props.attributeValuesAggMap[key]["attributeValue"]}</td>
                      <td>{props.attributeValuesAggMap[key]["count"]}</td>
                    </tr>
                  ))}
                  </tbody>
                </Table>
              </div>
            </Container>
          </Col>
        </Row>
      </Container>}
      {!props.attributeValuesAggMap || props.attributeValuesAggMap.length === 0
      && <div><p className="search-msg">No {props.content.toLowerCase()} found</p></div>}
    </>
  );
}