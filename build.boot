(set-env!
 :source-paths #{"src"}
 :resource-paths #{"asset"}
 :dependencies
 '[[adzerk/boot-cljs                        "2.0.0"]
   [org.clojure/core.async                  "0.3.443"]
   [org.clojure/clojure                     "1.9.0-alpha17"]
   [org.clojure/clojurescript               "1.9.562"]
   [org.clojure/test.check                  "0.9.0" :scope "test"]
   [org.clojure/tools.logging               "0.4.0"]
   [org.omcljs/om                           "1.0.0-beta1"]])

(#'clojure.core/load-data-readers)
(set! *data-readers* (.getRawRoot #'*data-readers*))

(require '[adzerk.boot-cljs      :refer [cljs]])

(task-options!
 cljs      {:compiler-options {:language-in :ecmascript5-strict}
            :optimizations :advanced})

(deftask deps [] (repl :server true))

(deftask package-extension
  "Builds cljs and code for production"
  []
  (with-pre-wrap fileset
    (dosh "./build_crx.sh")
    fileset))

(deftask build
  "Builds cljs code for production"
  []
  (comp
   (cljs)
   (target)))

(deftask build-extension
  "Build this extension for production"
  []
  (comp
   (build)
   (package-extension)))

(deftask push-extension
  "Build and push this extension to production"
  []
  (comp
   (build-extension)
   (dosh "./push_extension.py")))
