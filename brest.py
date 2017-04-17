# -*-coding:utf-8 -*-
import requests
import json
import csv
class Spider(object):
    json_url = "http://s.taobao.com/search?data-key=s&data-value=44&ajax=true&_KsTS=1479917597216_854&callback&q={}"
    def __init__(self,keyword):
        self.url = self.json_url.format(keyword)
        data = self.get_source()
        
        result_list=self.get_all_data(data)
        self.write_data(result_list)
    
    def get_source(self):
        html = requests.get(self.url)
        da = html.content
        return da.decode('utf-8')
                
        
    
    def get_all_data(self,data):
        data_dict = json.loads(data)
        
        item_list = data_dict['mods']['itemlist']['data']['auctions']
        print(item_list)
        result_list = []
        for item in item_list:
            result_dict = {}
            result_dict['title'] = item['title'].replace('<span class=H>','').replace('</span>','')
            result_dict['url'] = 'http:'+item['detail_url']
            result_dict['location'] = item['item_loc']
            result_dict['shop_name'] = item['nick']
            result_dict['付款人数'] = item['view_sales']
            result_dict['现价'] = ["view_price"]
            print result_dict
            result_list.append(result_dict)
        return result_list
    def write_data(self,result_list):
        with open('result.csv','w') as f:
            writer = csv.DictWriter(f,fieldnames =['title','付款人数','现价','shop_name','location','url'])
            writer.writeheader()
            writer.writerows(result_list)
            
            
if __name__ =="__main__":
    keyword = raw_input("input:")
    all_data = Spider(keyword)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            