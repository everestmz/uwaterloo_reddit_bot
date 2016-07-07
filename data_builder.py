from tools.helpers import bulk_add_to_data, load_json_into_array
from tools.s3 import update_json
from troll_comments import data_builder as troll_builder
from troll_comments import classifier as troll_classifier

def build_troll_comment_data():
    data = load_json_into_array('troll_comments/troll_training_data.json')['comments']
    threads = load_json_into_array('troll_comments/threads.json')['threads']

    while True:
        print "0) Exit"
        print "1) Comment Stream [count]"
        print "2) Hot Post Comments [count]"
        print "3) Cherry Pick Thread"
        print "4) Test a phrase"
        print "5) Metrics"

        selection = raw_input("> ").split(' ')
        selection = map(int, selection)

        final_data = {}

        if selection[0] == 0:
            exit(0)
        elif selection[0] == 1:
           final_data = troll_builder.new_comment_loop(selection[1], threads, data)
        elif selection[0] == 2:
            final_data = troll_builder.get_hot_post_comments(selection[1], threads)
        elif selection[0] == 3:
            final_data = troll_builder.cherry_pick_thread(threads)
        elif selection[0] == 4:
            final_data = troll_classifier.classify_cmdline(data)
        elif selection[0] == 5:
            troll_classifier.print_metrics(data)
        else:
            continue

        if final_data != {}:
            update_json('troll', 'comments', final_data["data"])
            update_json('troll', 'threads', final_data["threads"])

def main():
    build_troll_comment_data()


if __name__ == "__main__":
    main()