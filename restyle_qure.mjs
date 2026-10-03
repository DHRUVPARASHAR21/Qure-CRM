import fs from 'node:fs/promises';
import { FileBlob, SpreadsheetFile } from '@oai/artifact-tool';

const root='C:/Users/pardh/OneDrive/Desktop/Qure';
const inputPath=`${root}/outputs/qure-life-sciences-crm-india/qure_india_life_sciences_crm.xlsx`;
const outputDir=`${root}/outputs/qure-life-sciences-crm-qure-styled`;
const file=await FileBlob.load(inputPath); const wb=await SpreadsheetFile.importXlsx(file);
const C={bg:'#0B1926',panel:'#0D1E2D',panel2:'#11283A',header:'#143145',line:'#24445A',white:'#F8FAFC',muted:'#94A3B8',coral:'#FF6B6B',teal:'#14B8A6',tealDark:'#0F766E',amber:'#F4B740'};
const sheetRanges={
 'Dashboard':'A1:AB33','Accounts':'A1:P30','Contacts':'A1:S110','Opportunities':'A1:O30','Outreach & Activities':'A1:K35','Research Sources':'A1:G130','How to Use':'A1:B14','Lists':'A1:I18'
};
function formatRange(sheet,range,style){sheet.getRange(range).format=style;}
function baseSheet(name){const s=wb.worksheets.getItem(name);s.showGridLines=false;s.tabColor=C.coral;formatRange(s,sheetRanges[name],{fill:C.panel,font:{name:'Aptos',size:10,color:C.white},verticalAlignment:'center'});return s;}
function sectionHeader(s,range){formatRange(s,range,{fill:C.header,font:{name:'Aptos',size:10,color:C.white,bold:true},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true,borders:{bottom:{style:'thin',color:C.coral}}});}
function title(s,lastCol){formatRange(s,`A1:${lastCol}1`,{fill:C.bg,font:{name:'Aptos Display',size:16,color:C.white,bold:true},verticalAlignment:'center'});formatRange(s,`A2:${lastCol}2`,{fill:C.bg,font:{name:'Aptos',size:10,color:C.muted,italic:true},verticalAlignment:'center'});formatRange(s,`A3:${lastCol}3`,{fill:C.bg,borders:{bottom:{style:'medium',color:C.coral}}});s.getRange('A1').format.rowHeight=28;s.getRange('A2').format.rowHeight=20;}
function alternatingRows(s,start,end,lastCol){for(let r=start;r<=end;r++){const fill=r%2===0?C.panel:C.panel2;formatRange(s,`A${r}:${lastCol}${r}`,{fill,font:{name:'Aptos',size:10,color:C.white},verticalAlignment:'center',borders:{bottom:{style:'thin',color:C.line}}});}}

// Dashboard: reader-facing operating view.
const dash=baseSheet('Dashboard'); title(dash,'AB');
sectionHeader(dash,'A5:B5'); sectionHeader(dash,'D5:E5'); sectionHeader(dash,'G5:H5'); sectionHeader(dash,'J5:K5'); sectionHeader(dash,'D14:E14'); sectionHeader(dash,'G14:H14');
alternatingRows(dash,6,13,'B'); alternatingRows(dash,6,11,'E'); alternatingRows(dash,6,9,'H'); alternatingRows(dash,6,11,'K'); alternatingRows(dash,15,20,'E'); alternatingRows(dash,15,18,'H');
formatRange(dash,'A6:A13',{font:{name:'Aptos',size:10,color:C.muted,bold:true},fill:C.panel});formatRange(dash,'B6:B13',{font:{name:'Aptos Display',size:12,color:C.white,bold:true},fill:C.header,horizontalAlignment:'right'});formatRange(dash,'B8',{fill:C.coral,font:{name:'Aptos Display',size:12,color:C.bg,bold:true}});formatRange(dash,'B12:B13',{fill:C.tealDark,font:{name:'Aptos Display',size:12,color:C.white,bold:true}});formatRange(dash,'D4:K4',{font:{name:'Aptos',size:10,color:C.muted,bold:true},fill:C.bg});
dash.getRange('A5:K20').format.borders={insideHorizontal:{style:'thin',color:C.line},bottom:{style:'thin',color:C.line}};

// Operational tables.
const tableSpecs=[['Accounts','P',30],['Contacts','S',110],['Opportunities','O',30],['Outreach & Activities','K',35],['Research Sources','G',130],['Lists','I',18]];
for(const [name,last,end] of tableSpecs){const s=baseSheet(name);title(s,last);sectionHeader(s,`A5:${last}5`);alternatingRows(s,6,end,last);s.getRange(`A5:${last}${end}`).format.borders={insideHorizontal:{style:'thin',color:C.line},bottom:{style:'thin',color:C.line}};s.getRange(`A6:${last}${end}`).format.wrapText=false;}

// Direct, accessible status treatment with text retained.
const acc=wb.worksheets.getItem('Accounts');formatRange(acc,'J6:J30',{fill:'#462B35',font:{name:'Aptos',size:10,color:C.white,bold:true}});formatRange(acc,'K6:K30',{fill:'#102B3C',font:{name:'Aptos',size:10,color:C.white}});formatRange(acc,'P6:P30',{fill:C.tealDark,font:{name:'Aptos',size:10,color:C.white,bold:true},horizontalAlignment:'right'});
const contacts=wb.worksheets.getItem('Contacts');formatRange(contacts,'J6:J105',{fill:'#102B3C',font:{name:'Aptos',size:10,color:C.white,bold:true},horizontalAlignment:'right'});formatRange(contacts,'R6:R105',{fill:C.tealDark,font:{name:'Aptos',size:10,color:C.white,bold:true},horizontalAlignment:'right'});formatRange(contacts,'P6:P105',{fill:C.tealDark,font:{name:'Aptos',size:10,color:C.white,bold:true}});for(let r=6;r<=105;r++){if(String(contacts.getRange(`P${r}`).values?.[0]?.[0]??'').startsWith('Unverified'))formatRange(contacts,`P${r}`,{fill:'#462B35',font:{name:'Aptos',size:10,color:C.white,bold:true}});}
const opp=wb.worksheets.getItem('Opportunities');formatRange(opp,'G6:G30',{fill:'#462B35',font:{name:'Aptos',size:10,color:C.white,bold:true}});formatRange(opp,'H6:H30',{fill:'#102B3C',font:{name:'Aptos',size:10,color:C.white,bold:true}});formatRange(opp,'I6:I30',{fill:C.tealDark,font:{name:'Aptos',size:10,color:C.white,bold:true},horizontalAlignment:'right'});formatRange(opp,'O6:O30',{fill:'#102B3C',font:{name:'Aptos',size:10,color:C.white,bold:true}});
const act=wb.worksheets.getItem('Outreach & Activities');formatRange(act,'I6:I35',{fill:'#462B35',font:{name:'Aptos',size:10,color:C.white,bold:true}});formatRange(act,'K6:K35',{fill:'#462B35',font:{name:'Aptos',size:10,color:C.white,bold:true}});for(let r=6;r<=35;r++){if(String(act.getRange(`I${r}`).values?.[0]?.[0]??'')==='Completed')formatRange(act,`I${r}`,{fill:C.tealDark,font:{name:'Aptos',size:10,color:C.white,bold:true}});if(String(act.getRange(`K${r}`).values?.[0]?.[0]??'')==='Complete')formatRange(act,`K${r}`,{fill:C.tealDark,font:{name:'Aptos',size:10,color:C.white,bold:true}});}
const src=wb.worksheets.getItem('Research Sources');formatRange(src,'G6:G130',{fill:'#102B3C',font:{name:'Aptos',size:10,color:C.white,bold:true}});for(let r=6;r<=130;r++){if(String(src.getRange(`G${r}`).values?.[0]?.[0]??'').startsWith('Unverified'))formatRange(src,`G${r}`,{fill:'#462B35',font:{name:'Aptos',size:10,color:C.white,bold:true}});}

// ReadMe: calm, text-forward guidance rather than a dense source table.
const how=baseSheet('How to Use');title(how,'B');sectionHeader(how,'A5:B5');alternatingRows(how,6,14,'B');formatRange(how,'A6:A14',{fill:C.header,font:{name:'Aptos',size:10,color:C.white,bold:true},verticalAlignment:'top',wrapText:true});formatRange(how,'B6:B14',{fill:C.panel2,font:{name:'Aptos',size:10,color:C.white},verticalAlignment:'top',wrapText:true});how.getRange('A5:B14').format.borders={insideHorizontal:{style:'thin',color:C.line},bottom:{style:'thin',color:C.line}};

// Make working sheets compact but breathable.
for(const [name,last,end] of tableSpecs){const s=wb.worksheets.getItem(name);s.getRange(`A5:${last}5`).format.rowHeight=30;s.getRange(`A6:${last}${end}`).format.rowHeight=20;}
dash.getRange('A5:K20').format.rowHeight=21;dash.getRange('A5:K5').format.rowHeight=26;dash.getRange('D14:H14').format.rowHeight=26;

wb.recalculate();await fs.mkdir(outputDir,{recursive:true});const out=await SpreadsheetFile.exportXlsx(wb);await out.save(`${outputDir}/qure_india_life_sciences_crm_qure_styled.xlsx`);
console.log((await wb.inspect({kind:'table',range:'Dashboard!A1:K20',include:'values,formulas',tableMaxRows:20,tableMaxCols:11})).ndjson);console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'formula error scan'})).ndjson);for(const [sheetName,range] of [['Dashboard','A1:AB33'],['Accounts','A1:P18'],['Contacts','A1:S18'],['Opportunities','A1:O18'],['Outreach & Activities','A1:K18'],['Research Sources','A1:G18'],['How to Use','A1:B14'],['Lists','A1:I18']]){const p=await wb.render({sheetName,range,scale:1});await fs.writeFile(`${outputDir}/${sheetName.replace(/[^A-Za-z]/g,'_')}.png`,new Uint8Array(await p.arrayBuffer()));}
