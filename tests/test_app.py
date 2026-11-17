from pathlib import Path
from playwright.sync_api import sync_playwright
import json,os,tempfile
root=Path(__file__).resolve().parents[1]
artifacts=Path(os.environ.get('TEST_ARTIFACT_DIR',str(Path(tempfile.gettempdir())/'rifa-pro-tests')));artifacts.mkdir(parents=True,exist_ok=True)
fixture=(Path(__file__).with_name('fixture.js')).read_text()
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_EXECUTABLE'),headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 def new_page(query=''):
  page=browser.new_page(viewport={'width':390,'height':844});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/cdn.jsdelivr.net/**',lambda route:route.fulfill(status=200,body=fixture,content_type='application/javascript'))
  page.route('http://127.0.0.1:8765/**',lambda route:route.fulfill(status=200,body=(root/'index.html').read_text(),content_type='text/html'));page.goto('http://127.0.0.1:8765/index.html'+query);page.errors=errors
  return page
 page=new_page('?r=campanha-teste')
 page.locator('#ticketGrid button').first.wait_for(timeout=5000)
 assert page.locator('.price-row').inner_text().find('1300')>=0
 assert page.evaluate("drawToISO('2026-12-20T20:00')")== '2026-12-20T23:00:00.000Z'
 assert page.evaluate("localDrawValue('2026-12-20T23:00:00.000Z')")== '2026-12-20T20:00'
 assert page.evaluate("csvCell('=HYPERLINK(1)')").startswith("\"'")
 assert page.evaluate("testDB.calls.filter(x=>x.table==='raffle_tickets').length")==3
 for width in [360,390,412,1280]:
  page.set_viewport_size({'width':width,'height':844})
  assert not page.evaluate('document.documentElement.scrollWidth > innerWidth'),(width,page.evaluate('document.documentElement.scrollWidth'))
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(artifacts/'campanha.png'),full_page=True)
 page.locator('[data-quantity="10"]').click();assert page.locator('#stickyTotal').inner_text()=='R$\xa050,00'
 page.locator('#stickyReserve').click();page.locator('#customerName').fill('Cliente fictício');page.locator('#customerPhone').fill('11999990000')
 page.locator('#confirmReserve').click();page.locator('#resultDialog[open]').wait_for()
 assert page.locator('#resultDetails').inner_text().find('50,00')>=0
 assert page.locator('#copyPix').is_visible()
 assert page.locator('#paymentActions a').get_attribute('href').startswith('https://wa.me/5511999990000?')
 assert page.evaluate("testDB.raffle_reservations.length")==3
 page.locator('[data-close="resultDialog"]').click()
 page.locator('[data-filter="all"]').click();page.locator('#numberSearch').fill('1300');assert page.locator('#ticketGrid button').count()==1
 page.locator('#numberSearch').fill('');page.locator('#nextPage').click();assert page.locator('#pageLabel').inner_text()=='Página 2 de 22'
 page.locator('[data-quantity="5"]').click();page.locator('#stickyReserve').click();page.locator('#customerName').fill('Cliente fictício');page.locator('#customerPhone').fill('11999990000')
 page.evaluate('testDB.failReserve=true');page.locator('#confirmReserve').click();page.wait_for_function("!document.querySelector('#confirmReserve').disabled")
 assert page.locator('#checkoutError').inner_text();assert page.locator('#customerName').input_value()=='Cliente fictício'
 assert not page.errors,page.errors
 print('PASS: public campaign, 1300-ticket pagination, responsive widths, reservation, Pix, WhatsApp, filters, network-error form preservation')
 admin=new_page('?testadmin=1');admin.locator('#campaigns .campaign').wait_for()
 assert admin.locator('#campaigns .campaign').count()==1
 assert admin.locator('.metric.featured strong').inner_text()=='R$\xa0600,00'
 for width in [360,390,412,1280]:
  admin.set_viewport_size({'width':width,'height':844});assert not admin.evaluate('document.documentElement.scrollWidth > innerWidth'),width
 admin.set_viewport_size({'width':390,'height':844});admin.screenshot(path=str(artifacts/'painel.png'),full_page=True)
 admin.locator('[data-res]').click();admin.locator('[data-paid]').wait_for()
 admin.on('dialog',lambda dialog:dialog.accept());admin.locator('[data-paid]').click()
 admin.wait_for_function("document.querySelector('.metric.featured strong').textContent.includes('690')")
 assert admin.locator('#resPane').is_visible()
 with admin.expect_download() as download:admin.locator('#exportCurrent').click()
 assert download.value.suggested_filename=='rifa-pro-reservas.csv'
 admin.locator('#newRaffle').click();admin.locator('#title').fill('Campanha nova de teste');admin.locator('#quantity').fill('9')
 admin.evaluate('testDB.failTickets=true');admin.locator('#saveRaffle').click();admin.wait_for_function("!document.querySelector('#saveRaffle').disabled")
 assert admin.evaluate("testDB.raffles.find(r=>r.title==='Campanha nova de teste').status")=='draft'
 assert admin.evaluate("testDB.calls.filter(c=>c.table==='raffles'&&c.mode==='update'&&c.payload.status==='published').length")==0
 admin.evaluate('testDB.failTickets=false');admin.locator('#saveRaffle').click();admin.wait_for_function("document.querySelectorAll('#campaigns .campaign').length===2")
 assert admin.evaluate("testDB.raffles.filter(r=>r.title==='Campanha nova de teste').length")==1
 assert admin.evaluate("testDB.raffles.find(r=>r.title==='Campanha nova de teste').status")=='published'
 assert admin.evaluate("testDB.raffle_tickets.filter(t=>t.raffle_id===testDB.raffles.find(r=>r.title==='Campanha nova de teste').id).length")==9
 assert not admin.errors,admin.errors
 print('PASS: owner isolation, real-total metrics, payment sync, CSV, failed generation stays draft, retry without duplicate campaign and complete publication')
 login=new_page();login.locator('#authView:not(.hidden)').wait_for();login.locator('#email').fill('cliente@example.com');login.locator('#password').fill('senhaerrada');login.locator('#authSubmit').click();login.wait_for_function("document.querySelector('#authMessage').textContent.length>0");assert not login.locator('#authSubmit').is_disabled();assert not login.errors,login.errors
 print('PASS: login error recovery')
 browser.close()
