import React from 'react';
import axios from 'axios';
import { RadioGroup, Radio } from 'react-radio-group';
import {
  Segment,
  Image,
  Button,
  Header,
  Grid,
  TextArea,
  Form,
  Divider
} from 'semantic-ui-react';
import '../../styles/App.css';

class HomePage extends React.Component {
  state = {};

  render() {
    return (
      <Segment
        style={{ backgroundColor: '', minHeight: 600, padding: '0em 0em' }}
        vertical
      >
        <Grid className='my-grid' columns={2}>
          <Grid.Row>
            <Grid.Column style={{ backgroundColor: '', margin: 'auto 0' }}>
              <div style={{ backgroundColor: '', margin: '4em' }}>
                <Header
                  style={{ fontSize: '3em' }}
                  inverted
                  icon
                  textAlign='left'
                >
                  Medical Image Segmentation
                </Header>
                <p
                  style={{
                    color: 'white',
                    fontSize: '1em',
                    marginBottom: '3em'
                  }}
                >
                  Chúng tôi mong muốn xây dựng và phát triển một ứng dụng với
                  phương pháp tiếp cận toàn diện và có thể mở rộng, dựa vào nền
                  tảng học máy, cho phép hoàn toàn tự động phát hiện và phân
                  đoạn khối u bằng cách sử dụng ảnh MRI trong lĩnh vực thần
                  kinh.
                </p>
                <p
                  style={{
                    background: '',
                    color: 'white',
                    fontSize: '1em',
                    marginBottom: '1em'
                  }}
                >
                  Dataset: BraTS 2018
                  <br />
                  Link: https://www.med.upenn.edu/sbia/brats2018/data.html
                </p>
                <Image
                  src={require('../../images/brats2018example.jpg')}
                  size='large'
                  alt={'just image'}
                  style={{ marginBottom: '1em' }}
                />
                <Button
                  inverted
                  basic
                  size='huge'
                  color='grey'
                  type='Submit'
                  onClick={e => console.log(e)}
                >
                  Liên hệ
                </Button>
              </div>
            </Grid.Column>

            <Grid.Column>
              <Form className='my-form' onSubmit={this.onFormSubmit}>
                <Form.Field>
                  <Header as='h1' inverted>
                    Upload ảnh y khoa cần phân đoạn
                  </Header>
                  {/* TODO: Fix this to upload image*/}
                  <TextArea
                    style={{ minHeight: '200px' }}
                    value={this.state.term}
                    placeholder='up hinh'
                    onChange={this.handleTextAreaChange}
                  />
                  <Divider horizontal></Divider>
                </Form.Field>
                <Form.Field>
                  <RadioGroup
                    name='accent'
                    selectedValue={this.state.accent}
                    onChange={this.handleChange}
                    style={{ margin: '20px' }}
                  >
                    <Grid columns='three' divided>
                      <Grid.Row>
                        <Grid.Column>
                          <label className='radio-label'>
                            <Radio value='model1' /> Model 1
                          </label>
                        </Grid.Column>
                        <Grid.Column>
                          <label className='radio-label'>
                            <Radio value='model2' /> Model 2
                          </label>
                        </Grid.Column>
                        <Grid.Column>
                          <label className='radio-label'>
                            <Radio value='model3' /> Model 3
                          </label>
                        </Grid.Column>
                      </Grid.Row>
                    </Grid>
                  </RadioGroup>
                </Form.Field>
                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'row',
                    height: '80px',
                    justifyContent: 'center',
                    alignItems: 'center',
                    backgroundColor: ''
                  }}
                >
                  <Button
                    style={{ padding: '20px' }}
                    inverted
                    sbasic
                    size='huge'
                    color='teal'
                    type='Submit'
                  >
                    Tiến hành segment
                  </Button>{' '}
                </div>
              </Form>
            </Grid.Column>
          </Grid.Row>
        </Grid>{' '}
        */
      </Segment>
    );
  }
}

export default HomePage;
