from tools.s3 import update_json, get_data
from troll_comments import data_builder as troll_builder
from troll_comments import classifier as troll_classifier
from comment_scores.data_builder import generate, cherry_pick_thread

def build_comment_score_data():
    threads = get_data('score', 'threads')

    while True:
        print "0) Exit"
        print "1) Comment stream [count]"
        print "2) Cherry Pick Thread [thread]"
        response = raw_input("> ").split(' ')
        response[0] = int(response[0])

        result = {"threads": [], "data": []}

        if response[0] == 0:
            break
        elif response[0] == 1:
            result = generate(int(response[1]), threads)
        elif response[0] == 2:
            result = cherry_pick_thread(response[1], threads)

        if result != {"threads": [], "data": []}:
            print "Yay data"
            update_json('score', 'comments', result['data'])
            update_json('score', 'threads', result['threads'])


def build_troll_comment_data():
    data = get_data('troll', 'comments')
    threads = get_data('troll', 'threads')

    while True:
        print "0) Exit"
        print "1) Comment Stream [count]"
        print "2) Hot Post Comments [count]"
        print "3) Cherry Pick Thread"
        print "4) Test a phrase"
        print "5) Metrics"
        print "6) Test thread trolliness [thread]"

        selection = raw_input("> ").split(' ')
        selection[0] = int(selection[0])

        final_data = {}

        if selection[0] == 0:
            break
        elif selection[0] == 1:
           final_data = troll_builder.new_comment_loop(int(selection)[1], threads, data)
        elif selection[0] == 2:
            final_data = troll_builder.get_hot_post_comments(int(selection)[1], threads)
        elif selection[0] == 3:
            final_data = troll_builder.cherry_pick_thread(threads)
        elif selection[0] == 4:
            final_data = troll_classifier.classify_cmdline(data)
        elif selection[0] == 5:
            troll_classifier.print_metrics(data)
        elif selection[0] == 6:
            print troll_classifier.trolliness(data, selection[1])
        else:
            continue

        if final_data != {}:
            update_json('troll', 'comments', final_data["data"])
            update_json('troll', 'threads', final_data["threads"])

def main():
    while True:
        print "0) Exit"
        print "1) Troll Comments"
        print "2) Comment Scores"
        selection = int(raw_input("> "))

        if selection == 0:
            exit(0)
        elif selection == 1:
            build_troll_comment_data()
        elif selection == 2:
            build_comment_score_data()

if __name__ == "__main__":
    main()