const app = (() => {
    return {
        init: () => {
            // fix Chart size hacker style = 500
            window.dispatchEvent(new Event('resize'));

            let currentPage = "intro";

            const element = {
                reactEntryPoint: document.querySelector("#react-entry-point"),

                // presentation page
                presentationSection: document.querySelector("#data-presentation-section"),
                presentationLanguageDropdown: document.querySelector("#presentation-language-dropdown"),
                presentationNgramDropdown: document.querySelector("#presentation-ngram-dropdown"),
                presentationBarGraph: document.querySelector("#presentation-bar-graph"),
                presentationPieGraph: document.querySelector("#presentation-pie-graph"),
                presentationSection: document.querySelector("#data-presentation-section"),
                presentationSectionLink: document.querySelector("#data-presentation"),

                analysisSection: document.querySelector("#data-analysis-section"),
                analysisCollapsible: document.querySelector("#analysis-collapsible"),
                analysisTextInput: document.querySelector("#analyse-text-input"),
                analysisLanguageDropdownText: document.querySelector("#analysis-language-dropdown-text"),
                analysisNgramDropdownText: document.querySelector("#analysis-ngram-dropdown-text"),
                analysisBarGraphText: document.querySelector("#analysis-bar-graph-text"),
                analysisPieGraphText: document.querySelector("#analysis-pie-graph-text"),

                analysisFileUploadInput: document.querySelector("#analyse-file-upload-input-container"),
                analysisLanguageDropdownFile: document.querySelector("#analysis-language-dropdown-file"),
                analysisNgramDropdownFile: document.querySelector("#analysis-ngram-dropdown-file"),
                analysisBarGraphFile: document.querySelector("#analysis-bar-graph-file"),
                analysisPieGraphFile: document.querySelector("#analysis-pie-graph-file"),

                analysisSectionLink: document.querySelector("#data-analysis"),
                projectIntroSection: document.querySelector("#project-intro-section"),
                projectIntroSectionLink: document.querySelector("#project-intro"),
                // tabs: document.querySelector(".tabs"),
                collapsible: document.querySelector(".collapsible"),
                helpBtn: document.querySelector("#helpBtn")
            }

            // initialize tabs
            M.AutoInit();

            const collapsibleInstance = M.Collapsible.init(element.collapsible, {onOpenStart: e=>{
                currentPage = "analysis-" + e.getAttribute("title")
                window.dispatchEvent(new Event('resize'));}});
            // const tabsInstance = M.Tabs.init(element.tabs, {swipeable: false, onShow: ()=>{window.dispatchEvent(new Event('resize'));}});
            
            // tabsInstance.select('tab-monograms');
            // tabsInstance.updateTabIndicator();

            let dataStep = 0;
            const createDataIntroAttribute = (hintText, element, className) => {
                element.setAttribute("data-step", String(dataStep++))
                element.setAttribute("data-intro", hintText)
                element.classList.add(className)
            }

            //create help elements for presentation page
            createDataIntroAttribute("W tej sekcji możesz przeglądać wszystkie dane wczytane w programie.", element.reactEntryPoint, "presentation-help" )
            createDataIntroAttribute("Tu możesz wybrać język.", element.presentationLanguageDropdown, "presentation-help" )
            createDataIntroAttribute("Ten dropdown pozwala wybrać ngram.", element.presentationNgramDropdown, "presentation-help" )
            createDataIntroAttribute("Graf pokazuje analizę ngramów w wybranym prze Ciebie języku.", element.presentationBarGraph, "presentation-help" )
            createDataIntroAttribute("Klikając na konkretny ngram uaktywniasz diagram ngramów.", element.presentationBarGraph.children[0].children[0].children[0].children[2], "presentation-help" )
            createDataIntroAttribute("Który wyświetli dane w tym miejscu.", element.presentationPieGraph, "presentation-help" )
            createDataIntroAttribute("Poniżej grafu możesz zmieniać liczbę wyświetlanych elementów.", element.presentationBarGraph.nextSibling, "presentation-help" )

            helpBtn.addEventListener("click", ()=>{
                let options = {
                    nextLabel: "Następny",
                    prevLabel: "Poprzedni",
                    skipLabel: "Pomiń",
                    doneLabel: "Koniec",
                }
                switch(currentPage){
                    case "analysis-text":
                    introJs(".analysis-text-help").setOptions(options).start();
                    break;

                    case "analysis-file":
                    introJs(".analysis-text-help").setOptions(options).start();
                    break;
                    
                    case "presentation":
                    introJs(".presentation-help").setOptions(options).start();
                    break;
                }
            })

            const showAnalysisSection = () => {
                currentPage = "analysis"
                helpBtn.style.display = "none"
                window.dispatchEvent(new Event('resize'));
                element.analysisSection.classList.remove("hide")
                element.presentationSection.classList.remove("hide")
                element.presentationSection.classList.add("hide")
                element.projectIntroSection.classList.remove("hide")
                element.projectIntroSection.classList.add("hide")
            }

            const showPresentationSection = () => {
                currentPage = "presentation"
                helpBtn.style.display = "inline-block"
                window.dispatchEvent(new Event('resize'));
                element.presentationSection.classList.remove("hide")
                element.analysisSection.classList.remove("hide")
                element.analysisSection.classList.add("hide")
                element.projectIntroSection.classList.remove("hide")
                element.projectIntroSection.classList.add("hide")
            }

            const showProjectIntroSection = () => {
                currentPage = "intro"
                helpBtn.style.display = "none"
                element.projectIntroSection.classList.remove("hide")
                element.analysisSection.classList.remove("hide")
                element.analysisSection.classList.add("hide")
                element.presentationSection.classList.remove("hide")
                element.presentationSection.classList.add("hide")
            }

            element.analysisSectionLink.addEventListener("click", () => {
                showAnalysisSection()
            })

            element.presentationSectionLink.addEventListener("click", () => {
                showPresentationSection()
            })
        
            element.projectIntroSectionLink.addEventListener("click", () => {
                showProjectIntroSection()
            })
            
            showProjectIntroSection()
            console.log("initComplete")
        }
    }

})()

let time = setInterval(() => {
    let test = document.querySelector("#main-container")
    if (test) {
        app.init();
        clearInterval(time)
    }
}, 1000)




