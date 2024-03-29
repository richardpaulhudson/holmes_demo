from pathlib import Path
import holmes_extractor as holmes
import os

class Helper:
    """This class handles serialization, initialization, formatting and various HTML snippets"""

    # Setup
    def setup_en_literature(self,ontology_path:Path,model_name:str, en_literature_dir:Path):
        ontology = holmes.Ontology(ontology_path)
        holmes_manager = holmes.Manager(model=model_name, ontology=ontology, number_of_workers=1, verbose=True)

        serialized_documents = {}
        for file in os.listdir(str(en_literature_dir)):
            if file.endswith("hdc"):
                label = file[:-4]
                long_filename = os.sep.join((str(en_literature_dir), file))
                with open(long_filename, "rb") as file:
                    contents = file.read()
                serialized_documents[label] = contents
        holmes_manager.register_serialized_documents(serialized_documents)

        return holmes_manager

    # Processing
    def format_topic_query_output(self, results, color_map):
        """Format results of the Topic Extraction"""

        output_list = []

        for result in results:
            og_text = result["text"]
            output_dict = {"label":result["document_label"], "rank":result["rank"], "answers":result["text_to_match"], "text":""}

            if len(result["answers"]) > 0:
                for answer in result["answers"]:
                    output_dict["answers"] += "<p class='answer'>"+og_text[answer[0]:answer[1]]+"</p>"
            else:
                output_dict["answers"] = ""

            last_index = 0
            for word_info in result["word_infos"]:
                
                background_color = f"style='background-color:{color_map[word_info[2]]}'"

                output_dict["text"] += og_text[last_index:word_info[0]-1]+f" <p class='text_mark' data-text='{word_info[4]}' {background_color}> "+og_text[word_info[0]:word_info[1]]+" </p> "
                last_index = word_info[1]+1

            output_list.append(output_dict)
        
        return output_list

    # HTML
    def central_text(self, text):
        """Central Header"""

        html = f"""<h2 class='central_text'>{text}</h2>"""
        return html

    def card(self, n, text):
        """HTML Card"""

        html = f"""
        <div class='kpi'>
            <h4 class='card_text'>{n}<h4>
            <span>{text}</span>
        </div>
        """
        return html

    def topic_query_output(self, label, rank, text, answer):
        """HTML for Topic Extraction entries"""

        html = f"""
        <span class='rank'>{rank}</span> <span class='label'>{label}</span>
        <p class='text'>{text}</p>
        <p class='answer_container'>{answer}</p>
        """
        return html


