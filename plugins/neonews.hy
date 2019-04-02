
(import [xml.etree.cElementTree :as ETree])
(import requests)
(setv data (requests.get "http://feeds.reuters.com/reuters/topNews"))
(setv treetext ((. data text encode) "UTF-8") )
;;; (require hy.contrib.anaphoric)
;;; (list (ap-map (. it text) (tree.findall "./channel/item/title")))
;; (random.choice (list (ap-map (. it text) (tree.findall "./channel/item/title"))))

=> (defn format_item [item]
...  ((setv title (item.find "title"))
...   (setv link (item.find "link"))
...   (.format "{} | {}" title.text link.text)))
=> (format_item (random.choice (list (tree.findall "./channel/item"))))