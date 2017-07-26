import { ThesisFrontendPage } from './app.po';

describe('thesis-frontend App', () => {
  let page: ThesisFrontendPage;

  beforeEach(() => {
    page = new ThesisFrontendPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
